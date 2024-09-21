import math
from functools import cache

import torch
import torch.nn as nn
import torch.nn.functional as F

from einops import rearrange

from .base import LycorisBaseModule
from ..functional import factorization, rebuild_tucker
from ..functional.lokr import make_kron
from ..logging import logger
from ..utils.bnb import LinearNF4


@cache
def logging_force_full_matrix(lora_dim, dim, factor):
    logger.warning(
        f"lora_dim {lora_dim} is too large for"
        f" dim={dim} and {factor=}"
        ", using full matrix mode."
    )


class LokrModule(LycorisBaseModule):
    support_module = {
        "linear",
        "conv1d",
        "conv2d",
        "conv3d",
    }

    def __init__(
        self,
        lora_name,
        org_module: nn.Module,
        multiplier=1.0,
        lora_dim=4,
        alpha=1,
        dropout=0.0,
        rank_dropout=0.0,
        module_dropout=0.0,
        use_tucker=False,
        use_scalar=False,
        decompose_both=False,
        factor: int = -1,  # factorization factor
        rank_dropout_scale=False,
        weight_decompose=False,
        full_matrix=False,
        bypass_mode=False,
        rs_lora=False,
        unbalanced_factorization=False,
        **kwargs,
    ):
        super().__init__(
            lora_name,
            org_module,
            multiplier,
            dropout,
            rank_dropout,
            module_dropout,
            rank_dropout_scale,
            bypass_mode,
        )
        if self.module_type not in self.support_module:
            raise ValueError(f"{self.module_type} is not supported in LoKr algo.")

        factor = int(factor)
        self.lora_dim = lora_dim
        self.tucker = False
        self.use_w1 = False
        self.use_w2 = False
        self.full_matrix = full_matrix
        self.rs_lora = rs_lora

        if self.module_type.startswith("conv"):
            in_dim = org_module.in_channels
            k_size = org_module.kernel_size
            out_dim = org_module.out_channels
            self.shape = (out_dim, in_dim, *k_size)

            in_m, in_n = factorization(in_dim, factor)
            out_l, out_k = factorization(out_dim, factor)
            if unbalanced_factorization:
                out_l, out_k = out_k, out_l
            shape = ((out_l, out_k), (in_m, in_n), *k_size)  # ((a, b), (c, d), *k_size)
            self.tucker = use_tucker and any(i != 1 for i in k_size)
            if (
                decompose_both
                and lora_dim < max(shape[0][0], shape[1][0]) / 2
                and not self.full_matrix
            ):
                self.lokr_w1_a = nn.Parameter(torch.empty(shape[0][0], lora_dim))
                self.lokr_w1_b = nn.Parameter(torch.empty(lora_dim, shape[1][0]))
            else:
                self.use_w1 = True
                self.lokr_w1 = nn.Parameter(
                    torch.empty(shape[0][0], shape[1][0])
                )  # a*c, 1-mode

            if lora_dim >= max(shape[0][1], shape[1][1]) / 2 or self.full_matrix:
                if not self.full_matrix:
                    logging_force_full_matrix(lora_dim, max(in_dim, out_dim), factor)
                self.use_w2 = True
                self.lokr_w2 = nn.Parameter(
                    torch.empty(shape[0][1], shape[1][1], *k_size)
                )
            elif self.tucker:
                self.lokr_t2 = nn.Parameter(torch.empty(lora_dim, lora_dim, *shape[2:]))
                self.lokr_w2_a = nn.Parameter(
                    torch.empty(lora_dim, shape[0][1])
                )  # b, 1-mode
                self.lokr_w2_b = nn.Parameter(
                    torch.empty(lora_dim, shape[1][1])
                )  # d, 2-mode
            else:  # Conv2d not tucker
                # bigger part. weight and LoRA. [b, dim] x [dim, d*k1*k2]
                self.lokr_w2_a = nn.Parameter(torch.empty(shape[0][1], lora_dim))
                self.lokr_w2_b = nn.Parameter(
                    torch.empty(
                        lora_dim, shape[1][1] * torch.tensor(shape[2:]).prod().item()
                    )
                )
                # w1 ⊗ (w2_a x w2_b) = (a, b)⊗((c, dim)x(dim, d*k1*k2)) = (a, b)⊗(c, d*k1*k2) = (ac, bd*k1*k2)
        else:  # Linear
            in_dim = org_module.in_features
            out_dim = org_module.out_features
            self.shape = (out_dim, in_dim)

            in_m, in_n = factorization(in_dim, factor)
            out_l, out_k = factorization(out_dim, factor)
            if unbalanced_factorization:
                out_l, out_k = out_k, out_l
            shape = (
                (out_l, out_k),
                (in_m, in_n),
            )  # ((a, b), (c, d)), out_dim = a*c, in_dim = b*d
            # smaller part. weight scale
            if decompose_both and lora_dim < max(shape[0][0], shape[1][0]) / 2:
                self.lokr_w1_a = nn.Parameter(torch.empty(shape[0][0], lora_dim))
                self.lokr_w1_b = nn.Parameter(torch.empty(lora_dim, shape[1][0]))
            else:
                self.use_w1 = True
                self.lokr_w1 = nn.Parameter(
                    torch.empty(shape[0][0], shape[1][0])
                )  # a*c, 1-mode
            if lora_dim < max(shape[0][1], shape[1][1]) / 2:
                # bigger part. weight and LoRA. [b, dim] x [dim, d]
                self.lokr_w2_a = nn.Parameter(torch.empty(shape[0][1], lora_dim))
                self.lokr_w2_b = nn.Parameter(torch.empty(lora_dim, shape[1][1]))
                # w1 ⊗ (w2_a x w2_b) = (a, b)⊗((c, dim)x(dim, d)) = (a, b)⊗(c, d) = (ac, bd)
            else:
                self.use_w2 = True
                self.lokr_w2 = nn.Parameter(torch.empty(shape[0][1], shape[1][1]))

        self.wd = weight_decompose
        if self.wd:
            org_weight = org_module.weight.cpu().clone().float()
            self.dora_norm_dims = org_weight.dim() - 1
            self.dora_scale = nn.Parameter(
                torch.norm(
                    org_weight.transpose(1, 0).reshape(org_weight.shape[1], -1),
                    dim=1,
                    keepdim=True,
                )
                .reshape(org_weight.shape[1], *[1] * self.dora_norm_dims)
                .transpose(1, 0)
            ).float()

        self.dropout = dropout
        if dropout:
            print("[WARN]LoHa/LoKr haven't implemented normal dropout yet.")
        self.rank_dropout = rank_dropout
        self.rank_dropout_scale = rank_dropout_scale
        self.module_dropout = module_dropout

        if isinstance(alpha, torch.Tensor):
            alpha = alpha.detach().float().numpy()  # without casting, bf16 causes error
        alpha = lora_dim if alpha is None or alpha == 0 else alpha
        if self.use_w2 and self.use_w1:
            # use scale = 1
            alpha = lora_dim

        r_factor = lora_dim
        if self.rs_lora:
            r_factor = math.sqrt(r_factor)

        self.scale = alpha / r_factor

        self.register_buffer("alpha", torch.tensor(alpha))  # 定数として扱える

        if use_scalar:
            self.scalar = nn.Parameter(torch.tensor(0.0))
        else:
            self.scalar = torch.tensor(1.0)

        if self.use_w2:
            if use_scalar:
                torch.nn.init.kaiming_uniform_(self.lokr_w2, a=math.sqrt(5))
            else:
                torch.nn.init.constant_(self.lokr_w2, 0)
        else:
            if self.tucker:
                torch.nn.init.kaiming_uniform_(self.lokr_t2, a=math.sqrt(5))
            torch.nn.init.kaiming_uniform_(self.lokr_w2_a, a=math.sqrt(5))
            if use_scalar:
                torch.nn.init.kaiming_uniform_(self.lokr_w2_b, a=math.sqrt(5))
            else:
                torch.nn.init.constant_(self.lokr_w2_b, 0)

        if self.use_w1:
            torch.nn.init.kaiming_uniform_(self.lokr_w1, a=math.sqrt(5))
        else:
            torch.nn.init.kaiming_uniform_(self.lokr_w1_a, a=math.sqrt(5))
            torch.nn.init.kaiming_uniform_(self.lokr_w1_b, a=math.sqrt(5))

    def load_weight_hook(self, module: nn.Module, incompatible_keys):
        missing_keys = incompatible_keys.missing_keys
        for key in missing_keys:
            if "scalar" in key:
                del missing_keys[missing_keys.index(key)]
        if isinstance(self.scalar, nn.Parameter):
            self.scalar.data.copy_(torch.ones_like(self.scalar))
        elif getattr(self, "scalar", None) is not None:
            self.scalar.copy_(torch.ones_like(self.scalar))
        else:
            self.register_buffer(
                "scalar", torch.ones_like(self.scalar), persistent=False
            )

    def get_weight(self, shape):
        weight = make_kron(
            self.lokr_w1 if self.use_w1 else self.lokr_w1_a @ self.lokr_w1_b,
            (
                self.lokr_w2
                if self.use_w2
                else (
                    rebuild_tucker(self.lokr_t2, self.lokr_w2_a, self.lokr_w2_b)
                    if self.tucker
                    else self.lokr_w2_a @ self.lokr_w2_b
                )
            ),
            torch.tensor(self.scale),
        )
        dtype = weight.dtype
        if shape is not None:
            weight = weight.view(shape)
        if self.training and self.rank_dropout:
            drop = (torch.rand(weight.size(0)) > self.rank_dropout).to(dtype)
            drop = drop.view(-1, *[1] * len(weight.shape[1:]))
            if self.rank_dropout_scale:
                drop /= drop.mean()
            weight *= drop
        return weight

    def get_diff_weight(self, multiplier=1, shape=None, device=None):
        scale = self.scale * multiplier
        diff = self.get_weight(shape) * scale
        if device is not None:
            diff = diff.to(device)
        return diff, None

    def get_merged_weight(self, multiplier=1, shape=None, device=None):
        merged = (
            self.org_module[0].weight.data
            + self.get_diff_weight(multiplier=multiplier, shape=shape, device=device)[0]
        )
        if self.wd:
            merged = self.apply_weight_decompose(merged)
        return merged, None

    def apply_weight_decompose(self, weight):
        weight = weight.to(self.dora_scale.dtype)
        weight_norm = (
            weight.transpose(0, 1)
            .reshape(weight.shape[1], -1)
            .norm(dim=1, keepdim=True)
            .reshape(weight.shape[1], *[1] * self.dora_norm_dims)
            .transpose(0, 1)
        ) + torch.finfo(weight.dtype).eps

        return weight * (self.dora_scale / weight_norm)

    def custom_state_dict(self):
        destination = {}
        destination["alpha"] = self.alpha
        if self.wd:
            destination["dora_scale"] = self.dora_scale
        if self.use_w1:
            destination["lokr_w1"] = self.lokr_w1 * self.scalar
        else:
            destination["lokr_w1_a"] = self.lokr_w1_a * self.scalar
            destination["lokr_w1_b"] = self.lokr_w1_b

        if self.use_w2:
            destination["lokr_w2"] = self.lokr_w2
        else:
            destination["lokr_w2_a"] = self.lokr_w2_a
            destination["lokr_w2_b"] = self.lokr_w2_b
            if self.tucker:
                destination["lokr_t2"] = self.lokr_t2
        return destination

    @torch.no_grad()
    def apply_max_norm(self, max_norm, device=None):
        orig_norm = self.get_weight(self.shape).norm()
        norm = torch.clamp(orig_norm, max_norm / 2)
        desired = torch.clamp(norm, max=max_norm)
        ratio = desired.cpu() / norm.cpu()

        scaled = norm != desired
        if scaled:
            modules = 4 - self.use_w1 - self.use_w2 + (not self.use_w2 and self.tucker)
            if self.use_w1:
                self.lokr_w1 *= ratio ** (1 / modules)
            else:
                self.lokr_w1_a *= ratio ** (1 / modules)
                self.lokr_w1_b *= ratio ** (1 / modules)

            if self.use_w2:
                self.lokr_w2 *= ratio ** (1 / modules)
            else:
                if self.tucker:
                    self.lokr_t2 *= ratio ** (1 / modules)
                self.lokr_w2_a *= ratio ** (1 / modules)
                self.lokr_w2_b *= ratio ** (1 / modules)

        return scaled, orig_norm * ratio

    def bypass_forward_diff(self, h, scale=1):
        is_conv = self.module_type.startswith("conv")
        if self.use_w2:
            ba = self.lokr_w2
        else:
            a = self.lokr_w2_b
            b = self.lokr_w2_a

            if self.tucker:
                t = self.lokr_t2
                a = a.view(*a.shape, *[1] * (len(t.shape) - 2))
                b = b.view(*b.shape, *[1] * (len(t.shape) - 2))
            elif is_conv:
                a = a.view(*a.shape, *self.shape[2:])
                b = b.view(*b.shape, *[1] * (len(self.shape) - 2))

        if self.use_w1:
            c = self.lokr_w1
        else:
            c = self.lokr_w1_a @ self.lokr_w1_b
        uq = c.size(1)

        if is_conv:
            # (b, uq), vq, ...
            b, _, *rest = h.shape
            h_in_group = h.reshape(b * uq, -1, *rest)
        else:
            # b, ..., uq, vq
            h_in_group = h.reshape(*h.shape[:-1], uq, -1)

        if self.use_w2:
            hb = self.op(h_in_group, ba, **self.kw_dict)
        else:
            if is_conv:
                if self.tucker:
                    ha = self.op(h_in_group, a)
                    ht = self.op(ha, t, **self.kw_dict)
                    hb = self.op(ht, b)
                else:
                    ha = self.op(h_in_group, a, **self.kw_dict)
                    hb = self.op(ha, b)
            else:
                ha = self.op(h_in_group, a, **self.kw_dict)
                hb = self.op(ha, b)

        if is_conv:
            # (b, uq), vp, ..., f
            # -> b, uq, vp, ..., f
            # -> b, f, vp, ..., uq
            hb = hb.view(b, -1, *hb.shape[1:])
            h_cross_group = hb.transpose(1, -1)
        else:
            # b, ..., uq, vq
            # -> b, ..., vq, uq
            h_cross_group = hb.transpose(-1, -2)

        hc = F.linear(h_cross_group, c)
        if is_conv:
            # b, f, vp, ..., up
            # -> b, up, vp, ... ,f
            # -> b, c, ..., f
            hc = hc.transpose(1, -1)
            h = hc.reshape(b, -1, *hc.shape[3:])
        else:
            # b, ..., vp, up
            # -> b, ..., up, vp
            # -> b, ..., c
            hc = hc.transpose(-1, -2)
            h = hc.reshape(*hc.shape[:-2], -1)

        return self.drop(h * scale)

    def bypass_forward(self, x, scale=1):
        return self.org_forward(x) + self.bypass_forward_diff(x, scale=scale)

    def forward(self, x: torch.Tensor, *args, **kwargs):
        if self.module_dropout and self.training:
            if torch.rand(1) < self.module_dropout:
                return self.org_forward(x)
        if self.bypass_mode:
            return self.bypass_forward(x, self.multiplier)
        else:
            weight = (
                self.org_module[0].weight.data.to(self.dtype)
                + self.get_weight(self.shape) * self.scalar * self.multiplier
            )
            bias = (
                None
                if self.org_module[0].bias is None
                else self.org_module[0].bias.data
            )

            if self.wd:
                weight = self.apply_weight_decompose(weight)
            return self.op(x, weight, bias, **self.kw_dict)


if __name__ == "__main__":
    base = nn.Conv2d(128, 128, 3, 1, 1)
    net = LokrModule(
        "",
        base,
        multiplier=1,
        lora_dim=4,
        alpha=1,
        weight_decompose=False,
        use_tucker=False,
        use_scalar=False,
        decompose_both=True,
    )
    net.apply_to()
    sd = net.state_dict()
    for key in sd:
        if key != "alpha":
            sd[key] = torch.randn_like(sd[key])
    net.load_state_dict(sd)

    test_input = torch.randn(1, 128, 16, 16)
    test_output = net(test_input)
    print(test_output.shape)

    net2 = LokrModule(
        "",
        base,
        multiplier=1,
        lora_dim=4,
        alpha=1,
        weight_decompose=False,
        use_tucker=False,
        use_scalar=False,
        bypass_mode=True,
        decompose_both=True,
    )
    net2.apply_to()
    net2.load_state_dict(sd)
    print(net2)

    test_output2 = net(test_input)
    print(F.mse_loss(test_output, test_output2))

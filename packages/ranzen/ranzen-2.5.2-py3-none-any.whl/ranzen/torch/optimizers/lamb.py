from collections.abc import Iterable
import math
from typing_extensions import override

import torch
from torch import Tensor
from torch.optim.optimizer import Optimizer

from .common import LossClosure

__all__ = ["LAMB"]


class LAMB(Optimizer):
    r"""Implements the LAMB algorithm introduced in `Large Batch Optimization for Deep Learning`_.

    LAMB serves as the AdamW counterpart to the LARS optimizer, similarly employing layerwise
    adaptive learning rates train models effectively with large batch sizes.

    .. note::
        Implementation based on: https://github.com/cybertronai/pytorch-lamb

    :param params: iterable of parameters to optimize or dicts defining parameter groups.
    :param lr: learning rate.
    :param betas: coefficients used for computing running averages of gradient and its square.
    :param eps: term added to the denominator to improve numerical stability.
    :param weight_decay: weight decay coefficient.
    :param clamp_value: value to clamp the norm of the weights to.
    :param debias: whether to include the bias-correction term (1 - beta**step) from Adam.

    :raises ValueError: if any one of ``lr``, ``betas``, ``eps``, or ``weight_decay`` is not in
        its permitted range.

    .. _Large Batch Optimization for Deep Learning:
        https://arxiv.org/abs/1904.00962v5
    """

    def __init__(
        self,
        params: Iterable[Tensor],
        lr: float = 1e-3,
        betas: tuple[float, float] = (0.9, 0.999),
        *,
        eps: float = 1e-6,
        weight_decay: float = 0.0,
        clamp_value: float = 10.0,
        debias: bool = False,
    ) -> None:
        if lr <= 0.0:
            raise ValueError(f"Invalid learning rate: {lr}")
        if eps < 0.0:
            raise ValueError(f"Invalid epsilon value: {eps}")
        if not 0.0 <= betas[0] < 1.0:
            raise ValueError(f"Invalid beta parameter at index 0: {betas[0]}")
        if not 0.0 <= betas[1] < 1.0:
            raise ValueError(f"Invalid beta parameter at index 1: {betas[1]}")
        if weight_decay < 0:
            raise ValueError(f"Invalid weight_decay value: {weight_decay}")
        if clamp_value < 0.0:
            raise ValueError(f"Invalid clamp value: {clamp_value}")

        defaults = dict(lr=lr, betas=betas, eps=eps, weight_decay=weight_decay)
        self.clamp_value = clamp_value
        self.debias = debias

        super().__init__(params=params, defaults=defaults)

    @override
    def step(self, closure: LossClosure | None = None) -> Tensor | None:  # type: ignore
        r"""Performs a single optimization step.

        :param closure: A closure that reevaluates the model and returns the loss.
        :returns: loss returned by the closure if ``closure`` is not ``None`` else ``None``.

        :raises RuntimeError: if gradients are sparse.
        """
        loss = None
        if closure is not None:
            loss = closure()

        for group in self.param_groups:
            for p in group["params"]:
                if p.grad is None:
                    continue
                grad = p.grad.data
                if grad.is_sparse:
                    msg = (
                        "Lamb does not support sparse gradients, please consider SparseAdam instead"
                    )
                    raise RuntimeError(msg)

                state = self.state[p]

                # State initialization
                if len(state) == 0:
                    state["step"] = 0
                    # Exponential moving average of gradient values
                    state["exp_avg"] = torch.zeros_like(p)
                    # Exponential moving average of squared gradient values
                    state["exp_avg_sq"] = torch.zeros_like(p)

                exp_avg, exp_avg_sq = state["exp_avg"], state["exp_avg_sq"]
                beta1, beta2 = group["betas"]

                state["step"] += 1

                # Decay the first and second moment running average coefficient
                # m_t
                exp_avg.mul_(beta1).add_(grad, alpha=1 - beta1)
                # v_t
                exp_avg_sq.mul_(beta2).addcmul_(grad, grad, value=1 - beta2)

                # Paper v3 does not use debiasing.
                if self.debias:
                    bias_correction = math.sqrt(1 - beta2 ** state["step"])
                    bias_correction /= 1 - beta1 ** state["step"]
                else:
                    bias_correction = 1

                # Apply bias to lr to avoid broadcast.
                step_size = group["lr"] * bias_correction

                weight_norm = torch.norm(p.data).clamp(0, self.clamp_value)

                adam_step = exp_avg / exp_avg_sq.sqrt().add(group["eps"])
                if group["weight_decay"] != 0:
                    adam_step.add_(p.data, alpha=group["weight_decay"])

                adam_norm = torch.norm(adam_step)
                if weight_norm == 0 or adam_norm == 0:
                    trust_ratio = 1
                else:
                    trust_ratio = weight_norm / adam_norm
                state["weight_norm"] = weight_norm
                state["adam_norm"] = adam_norm
                state["trust_ratio"] = trust_ratio

                p.data.add_(adam_step, alpha=-step_size * trust_ratio)

        return loss

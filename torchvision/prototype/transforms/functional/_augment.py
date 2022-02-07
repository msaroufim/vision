from typing import Tuple
from typing import TypeVar

import torch
from torchvision.prototype import features
from torchvision.transforms import functional as _F

from .utils import dispatch

T = TypeVar("T", bound=features.Feature)


@dispatch
def erase(input: T, *, i: int, j: int, h: int, w: int, v: torch.Tensor, inplace: bool = False) -> T:
    """ADDME"""
    pass


erase_image = _F.erase
erase.register(features.Image, erase_image)


@dispatch
def mixup(input: T, *, lam: float, inplace: bool = False) -> T:
    """ADDME"""
    pass


def _mixup(input: torch.Tensor, batch_dim: int, lam: float, inplace: bool) -> torch.Tensor:
    if not inplace:
        input = input.clone()

    input_rolled = input.roll(1, batch_dim)
    return input.mul_(lam).add_(input_rolled.mul_(1 - lam))


def mixup_image(image_batch: torch.Tensor, *, lam: float, inplace: bool = False) -> torch.Tensor:
    if image_batch.ndim < 4:
        raise ValueError("Need a batch of images")

    return _mixup(image_batch, -4, lam, inplace)


mixup.register(features.Image, mixup_image)


def mixup_one_hot_label(one_hot_label_batch: torch.Tensor, *, lam: float, inplace: bool = False) -> torch.Tensor:
    if one_hot_label_batch.ndim < 2:
        raise ValueError("Need a batch of one hot labels")

    return _mixup(one_hot_label_batch, -2, lam, inplace)


mixup.register(features.OneHotLabel, mixup_one_hot_label)


@dispatch
def cutmix(
    input: T,
    *,
    box: Tuple[int, int, int, int] = dispatch.FEATURE_SPECIFIC_PARAM,  # type: ignore[assignment]
    lam_adjusted: float = dispatch.FEATURE_SPECIFIC_PARAM,  # type: ignore[assignment]
    inplace: bool = False,
) -> T:
    """ADDME"""
    pass


def cutmix_image(image_batch: torch.Tensor, *, box: Tuple[int, int, int, int], inplace: bool = False) -> torch.Tensor:
    if image_batch.ndim < 4:
        raise ValueError("Need a batch of images")

    if not inplace:
        image_batch = image_batch.clone()

    x1, y1, x2, y2 = box
    image_rolled = image_batch.roll(1, -4)

    image_batch[..., y1:y2, x1:x2] = image_rolled[..., y1:y2, x1:x2]
    return image_batch


cutmix.register(features.Image, cutmix_image)


def cutmix_one_hot_label(
    one_hot_label_batch: torch.Tensor, *, lam_adjusted: float, inplace: bool = False
) -> torch.Tensor:
    if one_hot_label_batch.ndim < 2:
        raise ValueError("Need a batch of one hot labels")

    return _mixup(one_hot_label_batch, -2, lam_adjusted, inplace)


cutmix.register(features.OneHotLabel, cutmix_one_hot_label)
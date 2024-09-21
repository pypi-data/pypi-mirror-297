from typing import Optional, Tuple
from collections.abc import Iterable
from math import pi

import torch


__all__ = [ 'hilbert_kernel' ]


def hilbert_kernel(
        intervals01: Iterable[torch.Tensor],
        intervals02: Iterable[torch.Tensor],
        /,
        *,
        range_intervals: Tuple[float, float] = (0.0, pi/2.0),
        paritial_info: bool = False
) -> torch.Tensor:

    

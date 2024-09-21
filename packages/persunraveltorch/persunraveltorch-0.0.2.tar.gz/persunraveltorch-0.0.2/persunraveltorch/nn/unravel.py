from typing import Tuple
from collections.abc import Iterable, Sequence
from math import pi

import itertools as it

import torch
import torch.nn as nn


__all__ = [ 'Unravel' ]


def _bool_to_sgn(val: bool) -> float:
    if val:
        return -1.0
    else:
        return  1.0


class Unravel(nn.Module):
    """Computes the associated unravelled persistence diagram.

    This module computes the unravelled persistence diagram
    associated to persistence intervals within a finite range
    :obj:`range_intervals`.

    Parameters
    ----------
    range_intervals : :class:`Tuple[float, float]`, optional
        The finite range containing all persistence intervals,
        defaults to :obj:`(0.0, pi/2.0)`.
    neg_x : :class:`bool`, optional
        Whether the x-axis is negated with respect to Cartesian coordintes,
        defaults to :obj:`False`
    neg_y : :class:`bool`, optional
        Whether the y-axis is negated with respect to Cartesian coordintes,
        defaults to :obj:`False`
    """

    def __init__(self,
                 *,
                 range_intervals: Tuple[float, float] = (0.0, pi/2.0),
                 neg_x: bool = False,
                 neg_y: bool = False,
                 device = None,
                 dtype = None
                 ) -> None:

        super().__init__()

        self._identity = torch.tensor(
            [[_bool_to_sgn(neg_x),                 0.0],
             [                0.0, _bool_to_sgn(neg_y)]
             ],
            device = device,
            dtype = dtype
        )

        self._reflection = torch.tensor(
            [[                0.0, _bool_to_sgn(neg_y)],
             [_bool_to_sgn(neg_x),                 0.0]
             ],
            device = device,
            dtype = dtype
        )

        min, max = range_intervals
        diff = min - max

        self._offsets = torch.tensor(
            [[_bool_to_sgn(neg_x) * diff,                        0.0],
             [                       0.0, _bool_to_sgn(neg_y) * diff]
             ],
            device = device,
            dtype = dtype
        )

        self._e1 = torch.tensor(
            [1.0, 0.0],
            device = device,
            dtype = dtype
        )

        self._e2 = torch.tensor(
            [0.0, 1.0],
            device = device,
            dtype = dtype
        )

        self._zero = torch.tensor(
            [0.0, 0.0],
            device = device,
            dtype = dtype
        )

    def forward(self,
                intervals: Iterable[torch.Tensor],
                /) -> Sequence[torch.Tensor]:
        """Computes the associated unravelled persistence diagram.

        Parameters
        ----------
        intervals : :class:`Iterable[torch.Tensor]`
            Persistence intervals by degree.

        Returns
        -------
        :class:`Sequence[torch.Tensor]`
            The associated unravelled persistence diagram.
        """

        reflection_powers = it.cycle( (self._identity, self._reflection) )
        offset_multipliers = it.accumulate(
            initial  = self._zero,
            iterable = it.cycle( (self._e1, self._e2) )
        )

        return [ intervals_d @ reflection_power +
                 offset_multiplier @ self._offsets
                 for
                 intervals_d,   reflection_power,  offset_multiplier in
                 zip(intervals, reflection_powers, offset_multipliers)
                 ]

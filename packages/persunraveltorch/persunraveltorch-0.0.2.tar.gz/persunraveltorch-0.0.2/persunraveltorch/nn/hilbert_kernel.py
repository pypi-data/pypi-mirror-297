from typing import Callable, Optional, Tuple
from collections.abc import Sequence

import itertools as it

from math import pi

import torch
from torch.nn.functional import relu


__all__ = [ 'HilbertKernel' ]


def _make_inner(f: Callable[[torch.nn.Module,
                             torch.Tensor,
                             torch.Tensor
                             ],
                            torch.Tensor]
                ) -> Callable[[torch.nn.Module,
                             torch.Tensor,
                             torch.Tensor
                             ],
                            torch.Tensor]:
    return lambda self, a, b: f(
        self,
        a.unsqueeze(-3),
        b.unsqueeze(-2)
    ).squeeze(-1).sum( dim = (-2, -1) )


class HilbertKernel(torch.nn.Module):
    """Kernel induced by the embedding as Hilbert functions.

    This is the kernel that is induced by the feature map
    that sends graded persistence intervals
    to the Hilbert function of the corresponding
    unravelled relative homology lattice
    using the inner product of square-integrable functions.

    Parameters
    ----------
    range_intervals : :class:`Tuple[float, float]`, optional
        The finite range containing all persistence intervals,
        defaults to :obj:`(0.0, pi/2.0)`.
    partial_info : :class:`bool`, optional
        If this is set to :obj:`True`,
        the inner product of the corresponding truncated Hilbert functions
        is computed.
        This is sensible,
        whenever persistence intervals are only known
        up to a certain degree.
        The corresponding attribute :attr:`partial_info`
        can be changed after initialization.
        The default is :obj:`False`.
    """
    
    def __init__(self,
                 *,
                 range_intervals: Tuple[float, float] = (0.0, pi/2.0),
                 partial_info: bool = False,
                 device = None,
                 dtype = None
                 ) -> None:

        super().__init__()

        min, max = range_intervals

        self.partial_info = partial_info
        """:class:`bool`:
        Whether Hilbert functions should be truncated
        before computing the inner product;
        also see the description of the corresponding parameter.
        """
        
        self._strip_width = torch.tensor(
            max - min,
            dtype = dtype,
            device = device
        )

        self._min = torch.tensor(
            min,
            dtype = dtype,
            device = device
        )
        
        self._zero = torch.tensor(
            0,
            dtype = dtype,
            device = device
        )
        
    @_make_inner
    def _area_same_degrees(self,
                           a: torch.Tensor,
                           b: torch.Tensor
                           ) -> torch.Tensor:
        join = torch.maximum( a, b )
        meet = torch.minimum( a, b )
        return (
            relu(
                meet.narrow( dim = -1, start = 1, length = 1 ) -
                join.narrow( dim = -1, start = 0, length = 1 )
            ) *
            relu(
                self._strip_width +
                meet.narrow( dim = -1, start = 0, length = 1 ) -
                join.narrow( dim = -1, start = 1, length = 1 )
            )
        )
            
    @_make_inner
    def _area_consecutive_degrees(self,
                                  a: torch.Tensor,
                                  b: torch.Tensor
                                  ) -> torch.Tensor:
        return (
            relu(
                torch.minimum(
                    b.narrow( dim = -1, start = 0, length = 1 ),
                    a.narrow( dim = -1, start = 1, length = 1 )
                ) -
                a.narrow( dim = -1, start = 0, length = 1 )
            ) *
            relu(
                b.narrow( dim = -1, start = 1, length = 1 ) -
                torch.maximum(
                    a.narrow( dim = -1, start = 1, length = 1 ),
                    b.narrow( dim = -1, start = 0, length = 1 )
                )
            )
        )

    @_make_inner
    def _area_last_degree_partial_info(self,
                                       a: torch.Tensor,
                                       b: torch.Tensor
                                       ) -> torch.Tensor:
        join = torch.maximum( a, b )
        meet = torch.minimum( a, b )
        return (
            relu(
                meet.narrow( dim = -1, start = 1, length = 1 ) -
                join.narrow( dim = -1, start = 0, length = 1 )
            ) *
            relu(
                meet.narrow( dim = -1, start = 0, length = 1 ) -
                self._min
            )
        )

    def _peel_off_residual(self,
                           intervals_pairs: Sequence[Tuple[torch.Tensor,
                                                           torch.Tensor]
                                                     ]
                           ) -> Tuple[Sequence[Tuple[torch.Tensor,
                                                     torch.Tensor]],
                                      torch.Tensor]:
        if self.partial_info:
            return (
                intervals_pairs[:-1],
                self._area_last_degree_partial_info(
                    *intervals_pairs[-1]
                )
            )
        else:
            return (
                intervals_pairs,
                self._zero
            )
                           
    def forward(self,
                intervals01: Sequence[torch.Tensor],
                intervals02: Sequence[torch.Tensor],
                /) -> torch.Tensor:
        """Computes the inner product of the corresponding Hilbert functions.

        Parameters
        ----------
        intervals01 : :class:`Sequence[torch.Tensor]`
            Persistence intervals
            for the first input
            as a :class:`Sequence[torch.Tensor]` by degree.
            So each item of this sequence
            is a :class:`torch.Tensor` of shape
            :math:`([\dots,] k, 2)`,
            where :math:`k` is the number of persistence intervals
            in the corresponding degree.
        intervals02 : :class:`Sequence[torch.Tensor]`
            Persistence intervals
            for the second input
            as a :class:`Sequence[torch.Tensor]` by degree
            analogous to the first parameter :obj:`intervals01`.

        Returns
        -------
        :class:`torch.Tensor`
            The inner product of the corresponding Hilbert functions.
        """

        intervals_pairs, residual = self._peel_off_residual(
            zip( intervals01, intervals02 )
        )

        return (
            sum( self._area_same_degrees(*intervals_pair) for
                 intervals_pair in intervals_pairs
                ) +
            sum( self._area_consecutive_degrees(*intervals_pair) for
                 intervals_pair in zip(intervals01, intervals02[1:])
                ) +
            sum( self._area_consecutive_degrees(*intervals_pair) for
                 intervals_pair in zip(intervals02, intervals01[1:])
                ) +
            residual
        )

from typing import Optional, Tuple
from math import pi

import torch
from torch.nn.functional import relu


__all__ = [ 'RasterTriangle' ]


def _scalar_product(u: torch.Tensor,
                    v: torch.Tensor,
                    /) -> torch.Tensor:

    return ( u.unsqueeze(-2) @ v.unsqueeze(-1) ).squeeze( (-2, -1) )


def _split_endpoints(intervals: torch.Tensor,
                     /) -> torch.Tensor:

        a_unsqueezed, b_unsqueezed = intervals.split( 1, dim = -1 )

        return (
            a_unsqueezed.squeeze( dim = -1 ),
            b_unsqueezed.squeeze( dim = -1 )
        )

    

class RasterTriangle(torch.nn.Module):
    """Rasters a triangle corresponding to a single patch of a biplane.

    This module takes persistence intervals within a finite range
    :obj:`range_intervals` of two consecutive degrees as input
    and rasters the corresponding single triangular patch
    to an unsheared biplane.

    Parameters
    ----------
    pixel_columns : :class:`int`
        The number of pixels used to raster each row or scanline
        of the strip supporting the relative homology lattice.
    range_intervals : :class:`Tuple[float, float]`, optional
        The finite range containing all persistence intervals,
        defaults to :obj:`(0.0, pi/2.0)`.
    max_overhead : :class:`Optional[int]`, optional
        If this is set,
        then the input will be processed in batches
        as small as necessary
        to limit the number of bytes allocated as overhead
        to at most :obj:`max_overhead`.
        So if you're not already processing your data
        in sufficiently small batches,
        setting this parameter is recommended.
        However,
        if the number of bytes required to process a single sample
        already exceeds :obj:`max_overhead`,
        the input is still processed sample by sample.
        The corresponding attribute :attr:`max_overhead`
        can be changed after initialization.
        The default is :obj:`None`.    
    """
    
    def __init__(self,
                 pixel_columns: int,
                 *,
                 range_intervals: Tuple[float, float] = (0.0, pi/2.0),
                 max_overhead: Optional[int] = None,
                 device = None,
                 dtype = None
                 ) -> None:

        super().__init__()

        self.max_overhead = max_overhead
        """:class:`Optional[int]`:
        Limits overhead as described for :class:`RasterTriangle`."""

        min, max = range_intervals

        strip_width = max - min
        side_len = strip_width / pixel_columns

        self._strip_width = torch.tensor(
            strip_width,
            dtype = dtype,
            device = device
        )

        self._side_len = torch.tensor(
            side_len,
            dtype = dtype,
            device = device
        )

        self._pixel_area = side_len * side_len

        self._px = torch.linspace(
            start = min,
            end = max - side_len,
            steps = pixel_columns,
            dtype = dtype,
            device = device
        )[:, None]

        self._py = torch.linspace(
            start = max - side_len,
            end = min,
            steps = pixel_columns,
            dtype = dtype,
            device = device
        )[:, None]

    @property
    def pixel_area(self) -> float:
        """:class:`float`: The area covered by each pixel."""
        return self._pixel_area

    def _outer_scalar_product(self,
                              u0: torch.Tensor,
                              v0: torch.Tensor,
                              /) -> torch.Tensor:

        if self.max_overhead is None:
            return _scalar_product( u0.unsqueeze(-2), v0.unsqueeze(-3) )
        
        u = u0.flatten( end_dim = -3 )
        v = v0.flatten( end_dim = -3 )

        split_size = max(
            1,
            self.max_overhead // (
                2 * u.shape[1] * v.shape[1] * v.shape[2] * u.element_size()
            )
        )
        
        us = torch.split( u[:, :, None, :], split_size )
        vs = torch.split( v[:, None, :, :], split_size )

        return torch.cat(
            [ _scalar_product(*pair) for pair in zip(us, vs) ]
        ).view(*u0.shape[:-1], v0.shape[-2])

    
    def _hilbert_function_integrals(self,
                                    x0: torch.Tensor,
                                    y0: torch.Tensor,
                                    /) -> torch.Tensor:
        x = x0.unsqueeze(dim=-2)
        y = y0.unsqueeze(dim=-2)
        
        hor_seg = relu(
            torch.minimum(
                self._side_len,
                torch.minimum(
                    self._px + self._side_len - x,
                    y - self._px
                )
            )
        )

        vert_seg = relu(
            torch.minimum(
                self._side_len,
                torch.minimum(
                    self._py + self._side_len - y,
                    x + self._strip_width - self._py
                )
            )
        )

        return self._outer_scalar_product( vert_seg, hor_seg )

    
    def _rank_invariant_integrals(self,
                                  x0: torch.Tensor,
                                  y0: torch.Tensor,
                                  /) -> torch.Tensor:
        x = x0.unsqueeze(dim=-2)
        y = y0.unsqueeze(dim=-2)
        
        hor_seg = relu(
            torch.minimum(
                self._side_len,
                self._px + self._side_len - x
            )
        )

        vert_seg = relu(
            torch.minimum(
                self._side_len,
                y - self._py
            )
        )

        return self._outer_scalar_product( vert_seg, hor_seg )

    
    def forward(self,
                intervals00: torch.Tensor,
                intervals01: torch.Tensor,
                /) -> torch.Tensor:
        """Triangle created from persistence intervals
        as described for :class:`RasterTriangle`.

        Parameters
        ----------
        intervals00 : :class:`torch.Tensor`
            Persistence intervals for the lower
            of the two consecutive degrees.
        intervals01 : :class:`torch.Tensor`
            Persistence intervals for the higher
            of the two consecutive degrees.

        Returns
        -------
        :class:`torch.Tensor`
            A triangle with two channels
            describing a single patch
            to an unsheared corresponding biplane.    
        """

        a0, b0 = _split_endpoints( intervals00 )
        a1, b1 = _split_endpoints( intervals01 )

        return torch.stack(
            dim = -3,
            tensors = [
                self._hilbert_function_integrals(
                    torch.cat(
                        ( a0, b1 - self._strip_width ),
                        dim = -1
                    ),
                    torch.cat(
                        ( b0, a1 ),
                        dim = -1
                    )
                ),
                self._rank_invariant_integrals(
                    a0,
                    b0
                )
            ]
        ) / self._pixel_area
        

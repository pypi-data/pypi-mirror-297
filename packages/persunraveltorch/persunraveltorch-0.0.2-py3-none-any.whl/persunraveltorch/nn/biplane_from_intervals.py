from typing import Optional, Tuple
from collections.abc import Iterable
from math import pi

import itertools as it

import torch

from .biplane_from_triangles import BiplaneFromTriangles
from .raster_triangle import RasterTriangle


__all__ = [ 'BiplaneFromIntervals' ]


class BiplaneFromIntervals(torch.nn.Module):
    r"""Creates a *biplane* from persistence intervals within a finite range.

    This module takes persistence intervals within a finite range
    :obj:`range_intervals` as an :class:`Iterable` by degree as input.
    So each item of the input is a :class:`torch.Tensor` of shape
    :math:`([\dots,] k, 2)`,
    where :math:`k` is the number of persistence intervals
    in the corresponding degree.
    The output can be thought of as a 3D bitmap with a depth of :math:`2`
    - henceforth called *biplane* -
    and two channels.
    So the output has shape :math:`([\dots,] 2, 2, w, h)`
    with the width :math:`w` being equal to
    :obj:`padding + pixel_columns + padding`.
    The :math:`0`-th channel contains two sheared rasterizations
    of the Hilbert function
    of the unravelled relative homology lattice
    on top of each other and offset
    by a glide reflection corresponding to suspension.
    Similarly, the :math:`1`-st channel contains two sheared rasterizations
    of the unravelled rank invariant
    on top of each other and offset
    by a glide reflection corresponding to suspension.

    Parameters
    ----------
    pixel_columns : :class:`int`
        The number of pixels used to raster each row or scanline
        of the strip supporting the relative homology lattice.
    range_intervals : :class:`Tuple[float, float]`, optional
        The finite range containing all persistence intervals,
        defaults to :obj:`(0.0, pi/2.0)`.
    padding : :class:`int`
        The amount of horizontal padding being added to both,
        the left and the right side.
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
        The default is :obj:`None`.
    """
    
    def __init__(self,
                 *,
                 pixel_columns: int,
                 range_intervals: Tuple[float, float] = (0.0, pi/2.0),
                 padding: int,
                 max_overhead: Optional[int] = None,
                 device = None,
                 dtype = None
                 ) -> None:

        super().__init__()

        self._no_intervals = torch.tensor(
            [],
            device = device,
            dtype = dtype
        )
        
        self.biplane_from_triangles = BiplaneFromTriangles(
            pixel_columns = pixel_columns,
            padding = padding,
            max_overhead = max_overhead,
            device = device,
            dtype = dtype
        )
        """:class:`BiplaneFromTriangles`:
        The instance used internally."""

        self.raster_triangle = RasterTriangle(
            pixel_columns = pixel_columns,
            range_intervals = range_intervals,
            max_overhead = max_overhead,
            device = device,
            dtype = dtype
        )
        """:class:`RasterTriangle`:
        The instance used internally."""

    @property
    def pixel_area(self) -> float:
        """:class:`float`: The area covered by each pixel."""
        return self.raster_triangle.pixel_area

    def forward(self,
                intervals: Iterable[torch.Tensor],
                /) -> torch.Tensor:
        """Biplane created from persistence intervals
        as described for :class:`BiplaneFromIntervals`.

        Parameters
        ----------
        intervals : :class:`Iterable[torch.Tensor]`
            Persistence intervals by degree.

        Returns
        -------
        :class:`torch.Tensor`
            A biplane with two channels
            describing the Hilbert function
            of the unravelled relative homology lattice
            and the unravelled rank invariant.
        """

        intervals_iterator = iter( intervals )
        
        intervals0 = next( intervals_iterator )
        no_intervals = self._no_intervals.view(
            intervals0.shape[:-2] + (0, 2)
        )

        return self.biplane_from_triangles(
            self.raster_triangle( *intervals_pair ) for
            intervals_pair in
            it.pairwise(
                it.chain( [intervals0],
                          intervals_iterator,
                          [no_intervals]
                         )
            )
        )
        

from typing import Optional
from collections.abc import Iterable

import itertools as it

import torch

from ._glue_to_fragment import GlueToFragment


__all__ = [ 'BiplaneFromTriangles' ]


class BiplaneFromTriangles(torch.nn.Module):
    """Asembles a biplane from triangles.

    This module takes triangles as created by :class:`RasterTriangle`
    as an input and assembles a biplane from these triangles.

    Parameters
    ----------
    pixel_columns : int
        The number of pixels used to raster each row or scanline
        of the strip assembled from triangles.
    max_overhead : Optional[int]
        If this is set,
        the input will be processed in batches
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
    padding : int
        The amount of horizontal padding being added to both,
        the left and the right side.
    """
    
    def __init__(self,
                 *,
                 pixel_columns: int,
                 padding: int,
                 max_overhead: Optional[int] = None,
                 device = None,
                 dtype = None
                 ) -> None:

        super().__init__()
        
        self._pixel_columns = pixel_columns
        self._padding       = padding
        
        self._glue_to_fragment = GlueToFragment(
            pixel_columns = pixel_columns,
            padding       = padding,
            max_overhead  = max_overhead
        )

        self._zero_triangle = torch.zeros(
            pixel_columns,
            pixel_columns
        )

        self._zero_fragment = torch.zeros(
            pixel_columns,
            pixel_columns + 2 * padding,
            dtype = dtype,
            device = device
        )

        self._pad_with_scanline = torch.nn.ZeroPad2d( (0, 0, 1, 1) )

    def forward(self,
                triangles: Iterable[torch.Tensor],
                /) -> torch.Tensor:
        """Asemble a biplane from triangles.

        Takes triangles as created by :class:`RasterTriangle`
        as an input and assembles a biplane from these triangles.

        Parameters
        ----------
        triangles : Iterable[torch.Tensor]
            Triangles as for example created by :class:`RasterTriangle`.

        Returns
        -------
        torch.Tensor
            A biplane assembled from `triangles`.
        """

        triangles_iterator = iter( triangles )

        triangle0 = next( triangles_iterator )

        zero_triangle = self._zero_triangle.view(
            (1,) * (len(triangle0.shape) - 2) + self._zero_triangle.shape
        ).expand( triangle0.shape )
        
        plane00_fragments: list[torch.Tensor] = []
        plane01_fragments: list[torch.Tensor] = []

        for pair_or_singleton in it.batched(
                n = 2,
                iterable = (
                    self._glue_to_fragment(*triangle_pair) for
                    triangle_pair in
                    it.pairwise(
                        it.chain(
                            [zero_triangle, triangle0],
                            triangles_iterator,
                            [zero_triangle]
                        )
                    )
                )
        ):
            
            plane01_fragments.append(
                pair_or_singleton[0]
            )
            plane00_fragments.append(
                ( pair_or_singleton + (self._zero_fragment,) )[1]
            )

        plane00 = torch.cat( plane00_fragments, dim = -2 )
        plane01 = torch.cat( plane01_fragments, dim = -2 )

        return self._pad_with_scanline(
            torch.stack( (plane00, plane01), dim = -3 )
        )

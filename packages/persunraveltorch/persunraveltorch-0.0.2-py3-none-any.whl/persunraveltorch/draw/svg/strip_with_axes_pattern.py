from typing import Any, Tuple
from dataclasses import dataclass
from math import sqrt

from .background_creator import BackgroundCreator
from ..strip_orientation import StripOrientation


__all__ = [ 'StripWithAxesPattern' ]


@dataclass(kw_only=True, slots=True)
class StripWithAxesPattern(BackgroundCreator):
    """Draws an axes pattern as a background.

    This :class:`BackgroundCreator` draws an axes pattern
    matching the regions of the unravelled relative homology lattice
    as a background.
    """

    large: float = 100
    """:class:`float`: Large number used for infinite shapes and lines."""
    
    line_width: float = 0.005
    
    tiles: int = 15
    """:class:`int`: The number of tiles to be drawn."""

    def __call__(self,
                 range_intervals: Tuple[float, float],
                 strip_orientation: StripOrientation,
                 **kwargs: Any
                 ):
        min, max = range_intervals
        strip_width = max - min

        ord = strip_orientation == StripOrientation.ORDINARY

        mult = 1 if ord else -1
        
        rect_mutual_attributes = (
            f'width="{strip_width * sqrt(0.5)}" '
            f'height="{self.large}" '
            f'transform="translate({min if ord else -max} {-max}) '
                       f'rotate({45 if ord else 315}) '
                       f'translate(0 {-0.5 * self.large})"'
        )
        
        points = ' '.join(
            ( f"{mult * (max - i * strip_width)},{i * strip_width - max} "
              f"{mult * (min - i * strip_width)},{i * strip_width - max}"
             ) for i in range(self.tiles)
        )
        
        return (
            f'<rect {rect_mutual_attributes} '
                   'fill="currentColor" '
                   'class="shade-095" />'
            f'<g stroke-width="{self.line_width * strip_width}" '
                'stroke="currentColor" '
                'class="shade-060" '
                'fill="none">'
              f'<rect {rect_mutual_attributes} />'
              f'<polyline points="{points}" '
                         'stroke-linejoin="bevel" '
                         'fill="none" />'
             '</g>'
        )


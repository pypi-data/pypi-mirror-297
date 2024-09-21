from typing import Any, Protocol, Tuple
from dataclasses import dataclass
from collections.abc import Sequence
from enum import StrEnum, auto

from .strip_orientation import StripOrientation


__all__ = [ 'Viewbox',
            'VerticalOrientation',
            'ViewboxCreator',
            'ViewboxWithPadding'
           ]


class VerticalOrientation(StrEnum):
    UP   = auto()
    DOWN = auto()


@dataclass(frozen=True, slots=True, kw_only=True)
class Viewbox:
    """Dataclass for attributes specifying a viewbox."""
    
    vertical_orientation: VerticalOrientation
    """:class:`VerticalOrientation`: Orientation of the y axis."""
    
    top: float
    right: float
    bottom: float
    left: float

    def __str__(self):
        or_down = self.vertical_orientation == VerticalOrientation.DOWN
        return (
            f"{self.left} {self.top if or_down else -self.top} "
            f"{self.right - self.left} {abs(self.top - self.bottom)}"
        )

    
class ViewboxCreator(Protocol):
    """Callable for creating a :class:`Viewbox` from parameters."""

    def __call__(self,
                 *,
                 range_intervals: Tuple[float, float],
                 strip_orientation: StripOrientation,
                 unravelled_intervals: Sequence,
                 **kwargs: Any
                 ) -> Viewbox:
        """Creates a :class:`Viewbox` from parameters.

        Parameters
        ----------
        range_intervals : :class:`Tuple[float, float]`
            The finite range containing all persistence intervals.
        strip_orientation : :class:`StripOrientation`
            The orientation of the strip to be drawn.
        unravelled_intervals : :class:`Sequence`
            The unravelled persistence intervals
            as a sequence by degree.
        **kwargs : :class:`Any`
            Any descendent of :class:`ViewboxCreator` needs this
            so the protocol can be extended in the future.

        Returns
        -------
        :class:`Viewbox`
        """
        ...
                 

def _maybe_flip_x(strip_orientation: StripOrientation,
                  left: float,
                  right: float
                  ) -> Tuple[float, float]:
    match strip_orientation:
        case StripOrientation.ORDINARY:
            return (left, right)
        case StripOrientation.CROSS:
            return (-right, -left)
        
        
@dataclass(kw_only=True, slots=True)
class ViewboxWithPadding(ViewboxCreator):
    """Creates a :class:`Viewbox` based on highest degree with padding."""

    padding: float
    """:class:`float`:
    The amount of padding to be added in local coordinates.
    """

    def __call__(self,
                 *,
                 range_intervals: Tuple[float, float],
                 strip_orientation: StripOrientation,
                 unravelled_intervals: Sequence,
                 **kwargs: Any
                 ) -> Viewbox:

        min, max = range_intervals
        strip_width = max - min

        padding = self.padding * strip_width
        
        left, right = _maybe_flip_x(
            strip_orientation = strip_orientation,
            left  = min - ( len(unravelled_intervals) // 2 ) * strip_width,
            right = max
        )
        
        return Viewbox(
            vertical_orientation = VerticalOrientation.UP,
            top = max + padding,
            right = right + padding,
            bottom = (
                max -
                ( (len(unravelled_intervals) + 1) // 2 ) * strip_width -
                padding
            ),
            left = left - padding,
        )
    

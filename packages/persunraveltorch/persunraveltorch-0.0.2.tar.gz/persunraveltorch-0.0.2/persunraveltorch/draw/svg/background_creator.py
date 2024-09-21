from typing import Any, Protocol, Tuple

from ..strip_orientation import StripOrientation


__all__ = [ 'BackgroundCreator' ]


class BackgroundCreator(Protocol):
    """Callable for drawing backgrounds."""

    def __call__(self,
                 *,
                 range_intervals: Tuple[float, float],
                 strip_orientation: StripOrientation,
                 **kwargs: Any
                 ) -> str:
        """Draws a background from parameters.

        Parameters
        ----------
        range_intervals : :class:`Tuple[float, float]`
            The finite range containing all persistence intervals.
        strip_orientation : :class:`StripOrientation`
            The orientation of the strip to be drawn.
        **kwargs : :class:`Any`
            Any descendent of :class:`BackgroundCreator` needs this
            so the protocol can be extended in the future.

        Returns
        -------
        :class:`str`
            The SVG code for the background.
        """
        ...



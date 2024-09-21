from typing import Any, Protocol
from dataclasses import dataclass

from .sizes import Length, Sizes, Unit
from ..viewbox import Viewbox


__all__ = [ 'Seizing',
            'SeizingByWidth',
            'SeizingByHeight'
           ]


class Seizing(Protocol):
    """Callable to obtain 'width' and 'height' from parameters."""

    def __call__(self,
                 *,
                 aspect_ratio: float,
                 viewbox: Viewbox,
                 complete_dimensions: bool,
                 **kwargs: Any
                 ) -> Sizes:
        """Computes 'width' and 'height' attributes from parameters.

        Parameters
        ----------
        aspect_ratio : :class:`float`
        viewbox : :class:`Viewbox`
        complete_dimensions : :class:`bool`
            Whether both attributes,
            'width' and 'height' should be specified.
        **kwargs : :class:`Any`
            Any descendent of :class:`Seizing` needs this
            so the protocol can be extended in the future.

        Returns
        -------
        :class:`Sizes`
            The resulting 'width' and/or 'height' attribute.
        """
        ...
        
        
@dataclass(kw_only=True, slots=True)
class SeizingByWidth(Seizing):
    """Computes 'width' and 'height' attributes from a specified width."""

    length: Length
    """:class:`Length`: The length of the specified width."""

    def __call__(self,
                 *,
                 aspect_ratio: float,
                 complete_dimensions: bool,
                 **kwargs: Any
                 ) -> Sizes:

        value, unit = self.length
        
        if complete_dimensions and unit != Unit.PERCENT:
            return Sizes(
                width  = self.length,
                height = Length(
                    value = value / aspect_ratio,
                    unit  = unit
                )
            )
        else:
            return Sizes( width = self.length )

                
@dataclass(kw_only=True, slots=True)
class SeizingByHeight(Seizing):
    """Computes 'width' and 'height' attributes from a specified height."""

    length: Length
    """:class:`Length`: The length of the specified height."""

    def __call__(self,
                 *,
                 aspect_ratio: float,
                 complete_dimensions: bool,
                 **kwargs: Any
                 ) -> Sizes:

        value, unit = self.length
        
        if complete_dimensions and unit is not Unit.PERCENT:
            return Sizes(
                height = self.length,
                width  = Length(
                    value = value * aspect_ratio,
                    unit  = unit
                )
            )
        else:
            return Sizes( height = self.length )

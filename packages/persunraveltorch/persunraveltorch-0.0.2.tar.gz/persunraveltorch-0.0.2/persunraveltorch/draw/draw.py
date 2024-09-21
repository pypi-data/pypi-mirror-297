from typing import ClassVar, Optional, Tuple
from collections.abc import Callable, Iterable, Sequence
from importlib import import_module
from math import pi
import io

import torch
import numpy as np

from . import css, svg
from .seizing import Length, Seizing, SeizingByHeight, Unit
from .strip_orientation import StripOrientation
from .viewbox import ViewboxCreator, ViewboxWithPadding

from ..nn import Unravel


__all__ = [ 'Draw', 'SVG' ]


class SVG(str):
    """SVG as a string that is automatically displayed as such in Jupyter."""
    def _repr_svg_(self):
        return self
    def _repr_html_(self):
        return self


class Draw:
    """Callable drawing unravelled persistence diagrams as :class:`SVG`.

    Parameters
    ----------
    range_intervals : :class:`Tuple[float, float]`, optional
        See :attr:`range_intervals` for details,
        defaults to :obj:`(0.0, pi/2.0)`.
    seizing : :class:`Seizing`, optional
        See :attr:`seizing` for details.
        The default is an instance of :class:`SeizingByHeight`,
        specifically :obj:`SeizingByHeight( length = Length(650.0, Unit.PX) )`.
    viewbox_creator : :class:`ViewboxCreator`, optional
        See :attr:`viewbox_creator` for details,
        defaults to :obj:`ViewboxWithPadding( padding=0.06 )`.
    strip_orientation : :class:`StripOrientation`, optional
        The orientation of the strip to be drawn,
        see also :attr:`strip_orientation`.
        The default is :obj:`StripOrientation.ORDINARY`,
        :obj:`StripOrientation.CROSS` can be a sensible choice
        for functional or extended persistence.
    background_creator : :class:`svg.BackgroundCreator`, optional
        Draws the background based on the input,
        see also :attr:`background_creator`.
        The default is a default instance of :class:`svg.StripWithAxesPattern`.
    unravel : :class:`Optional[ Callable ]`, optional
        If this is not :obj:`None`,
        then it is used to compute unravelled persistence diagrams
        instead of a newly created instance of :class:`Unravel`,
        see also :attr:`unravel`.
        The default is :obj:`None`.
    fmt : :class:`str`, optional
        See :attr:`fmt` for details,
        defaults to '%.5f'.
    """

    stylesheet: ClassVar[str] = css.POLYLINE + css.LIGHT_SCHEME
    """:class:`str`:
    The stylesheet to be used by the SVG.

    The initial value is the concatenation of
    :obj:`css.POLYLINE` and :obj:`css.LIGHT_SCHEME`.
    """
    
    defs: ClassVar[str] = svg.MARKERS
    """:class:`str`:
    SVG code to be wrapped by a <defs> element.

    The initial value is :obj:`svg.MARKERS`.
    """
    
    standalone: ClassVar[bool] = True
    """:class:`bool`: If drawn SVGs should be standalone (by default)."""

    __slots__ = ('range_intervals',
                 'seizing',
                 'viewbox_creator',
                 'strip_orientation',
                 'background_creator',
                 'fmt',
                 'unravel' 
                 )

    def __init__(
            self,
            *,
            range_intervals: Tuple[float, float] = (0.0, pi/2.0),
            seizing: Seizing = SeizingByHeight(
                length = Length(650.0, Unit.PX) ),
            viewbox_creator: ViewboxCreator = ViewboxWithPadding(
                padding=0.06 ),
            strip_orientation: StripOrientation = StripOrientation.ORDINARY,
            background_creator: svg.BackgroundCreator = (
                svg.StripWithAxesPattern()
            ),
            unravel: Optional[ Callable ] = None,
            fmt: str = '%.5f',
            device = None,
            dtype = None):
        
        self.range_intervals = range_intervals
        """:class:`Tuple[float, float]`:
        The finite range containing all persistence intervals.
        """
        
        self.seizing = seizing
        """:class:`Seizing`:
        Computes 'width' and 'height' attributes based on the input.
        """
        
        self.viewbox_creator = viewbox_creator
        """:class:`ViewboxCreator`: Creates a viewbox based on the input."""
        
        self.strip_orientation = strip_orientation
        """:class:`StripOrientation`:
        The orientation of the strip to be drawn.
        """
        
        self.background_creator = background_creator
        """:class:`svg.BackgroundCreator`:
        Draws the background based on the input.
        """
        
        self.fmt = fmt
        """:class:`str`:
        The format string used to render floats into strings.
        """
        
        self.unravel = Unravel(
            range_intervals = range_intervals,
            neg_x = (
                False if
                strip_orientation == StripOrientation.ORDINARY else
                True
            ),
            neg_y = True,
            device = device,
            dtype = dtype
        ) if unravel is None else unravel
        """:class:`Optional[ Callable ]`:
        Used to compute unravelled persistence diagrams."""

    @classmethod
    def complement_notebook(cls):
        """Complements the notebook with CSS and SVG containing 'defs'.

        This classmethod is supposed to be called from Jupyter Notebook.
        It adds a <style> element wrapping :attr:`stylesheet`
        and an invisible <svg> containing a <defs> element wrapping
        :attr:`defs` to the notebook.
        Moreover,
        it has the side effect of setting :attr:`standalone` to :obj:`False`.
        """
        try:
            ipython_display_mod = import_module('IPython.display')
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "The method 'complement_notebook' is intended to be called "
                "from Jupyter Notebook."
            )

        ipython_display_mod.display(
            ipython_display_mod.HTML(
                f'<style>{cls.stylesheet}</style>'
                 '<svg width="0" '
                      'height="0" '
                      'style="position: absolute; z-index: -1">'
                  f'<defs>{cls.defs}</defs>'
                 '</svg>'
                 "CSS and an SVG with 'defs' were added to the DOM."
                 "<br>"
                 "In order for this to take any effect "
                 "you may have to press this button: "
                 "<button>Activate CSS and SVG 'defs'</button>"
            )
        )
        cls.standalone = False

    def _unravel(self,
                 intervals: Sequence[ torch.Tensor | Iterable[torch.Tensor] ]
                 ) -> Tuple[ Sequence[torch.Tensor | Sequence[torch.Tensor]],
                             Sequence[Sequence[torch.Tensor]] ]:
        if isinstance(intervals[0], torch.Tensor):
            unravelled_intervals_degreewise = self.unravel(intervals)
            return (
                unravelled_intervals_degreewise,
                list( zip(*unravelled_intervals_degreewise) )
            )
        else:
            unravelled_intervals_batchwise = [
                self.unravel(intervals_b) for intervals_b in intervals
            ]
            return (
                list( zip(*unravelled_intervals_batchwise) ),
                unravelled_intervals_batchwise
            )

    def _style_n_defs(self,
                      standalone: bool
                      ) -> str:
        if standalone:
            return (
                f'<style>{self.stylesheet}</style>'
                f'<defs>{self.defs}</defs>'                
            )
        else:
            return ''

    def _unr_ints_d_to_str(self,
                           unravelled_intervals_d: torch.Tensor
                           ) -> str:
        with io.StringIO() as txt_stream:
            np.savetxt(txt_stream,
                       unravelled_intervals_d.numpy(),
                       fmt = self.fmt,
                       delimiter = ',',
                       newline = ' '
                       )
            return txt_stream.getvalue()

    def _create_polyline(self,
                         unravelled_intervals: Iterable[torch.Tensor]
                         ) -> str:
        points = ' '.join(
            self._unr_ints_d_to_str( unravelled_intervals_d ) for
            unravelled_intervals_d in
            unravelled_intervals
        )
        return f'<polyline points="{points}" />'

    
    def __call__(self,
                 intervals: Sequence[ torch.Tensor | Iterable[torch.Tensor] ],
                 *,
                 seizing: Optional[Seizing] = None,
                 viewbox_creator: Optional[ViewboxCreator] = None,
                 standalone: Optional[bool] = None,
                 complete_dimensions: Optional[bool] = None,
                 ) -> SVG:
        """Draws unravelled persistence diagram as :class:`SVG`.

        Parameters
        ----------
        intervals : :class:`Sequence[ torch.Tensor | Iterable[torch.Tensor] ]`
            Persistence intervals.
            If a :class:`Sequence[torch.Tensor]` is passed,
            the indices of the outer sequence correspond to degrees,
            whereas if a
            :class:`Sequence[Iterable[torch.Tensor]]`
            is passed,
            then the inner :class:`Iterable` is assumend to correspond
            to the degrees
            and the outer :class:`Sequence` corresponds to different
            persistence diagrams.
        seizing : :class:`Optional[Seizing]`, optional
            If this is not :obj:`None`,
            then it is used in place of :attr:`seizing`,
            defaults to :obj:`None`.
        viewbox_creator : :class:`Optional[ViewboxCreator]`, optional
            If this is not :obj:`None`,
            then it is used in place of :attr:`viewbox_creator`,
            defaults to :obj:`None`.
        standalone : :class:`Optional[bool]`, optional
            If this is not :obj:`None`,
            then it is used in place of :attr:`standalone`,
            defaults to :obj:`None`.
        complete_dimensions : :class:`Optional[bool]`
            If this is not :obj:`None`,
            then it is used in place of :attr:`complete_dimensions`,
            defaults to :obj:`None`.

        Returns
        -------
        :class:`SVG`
            The SVG picturing unravelled persistence diagrams.
        """

        seizing = self.seizing if seizing is None else seizing
        viewbox_creator = (
            self.viewbox_creator if
            viewbox_creator is None else
            viewbox_creator
        )
        standalone = self.standalone if standalone is None else standalone

        ( unravelled_intervals_degreewise,
          unravelled_intervals_batchwise ) = self._unravel( intervals )

        viewbox = viewbox_creator(
            range_intervals = self.range_intervals,
            strip_orientation = self.strip_orientation,
            unravelled_intervals = unravelled_intervals_degreewise
        )

        sizes = seizing(
            aspect_ratio = ( viewbox.right - viewbox.left ) / abs(
                viewbox.top - viewbox.bottom
            ),
            viewbox = viewbox,
            complete_dimensions = (
                standalone if
                complete_dimensions is None else
                complete_dimensions
            )
        )

        background = self.background_creator(
            range_intervals = self.range_intervals,
            strip_orientation = self.strip_orientation
        )

        polylines = ''.join(
            self._create_polyline( unravelled_intervals_b ) for
            unravelled_intervals_b in
            unravelled_intervals_batchwise
        )
        
        return SVG(
            f'<svg {sizes} '
                 f'viewBox="{viewbox}" '
                  'xmlns="http://www.w3.org/2000/svg">'
              f'{self._style_n_defs(standalone)}'
              f'{background}'
              f'<g class="unravelled-diagrams">{polylines}</g>'
             '</svg>'
        )

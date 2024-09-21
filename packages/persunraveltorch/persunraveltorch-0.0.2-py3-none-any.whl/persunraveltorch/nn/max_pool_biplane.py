from typing import Optional

import torch

from ._kernel_sizes import _size_2_t

from .functional import max_pool_biplane


__all__ = [ 'MaxPoolBiplane' ]


class MaxPoolBiplane(torch.nn.Module):
    """Essentialy :class:`torch.nn.MaxPool2d` with more flexible broadcasting.

    This works almost the same as :class:`torch.nn.MaxPool2d`
    except that it has more flexible broadcasting behaviour
    to accomodate processing biplanes.

    Parameters
    ----------
    kernel_size : :class:`int | Tuple[int, int]`
        The size of the window to take max over.
    stride : :class:`Optional[ int | Tuple[int, int] ]`, optional
        The stride of the window, defaults to :obj:`None`.
    padding : :class:`int | Tuple[int, int]`, optional
        Implicit negative infinity padding to be added on both sides,
        defaults to :obj:`0`.
    dilation : :class:`int | Tuple[int, int]`, optional
        This parameter controls the stride of elements in the window,
        defaults to :obj:`1`.
    return_indices : :class:`bool`, optional
        If this is set to :obj:`True`,
        tnen the max indices will be returned with the output.
        The default is :obj:`False`.
    ceil_mode : :class:`bool`, optional
        If this is set to :obj:`True`,
        then :func:`ceil` instead of :func:`floor`
        will be used to compute the output shape.
        The default is :obj:`False`.
    """
    
    def __init__(self,
                 kernel_size: _size_2_t,
                 stride: Optional[_size_2_t] = None,
                 padding:  _size_2_t = 0,
                 dilation: _size_2_t = 1,
                 return_indices: bool = False,
                 ceil_mode: bool = False
                 ) -> None:

        super().__init__()

        self._max_pool_kwargs = dict(
            kernel_size = kernel_size,
            stride = stride,
            padding = padding,
            dilation = dilation,
            return_indices = return_indices,
            ceil_mode = ceil_mode
        )
        
    def forward(self,
                input: torch.Tensor,
                /) -> torch.Tensor:
        """Applies max pooling as described for :class:`MaxPoolBiplane`.

        Parameters
        ----------
        input : :class:`torch.Tensor`
            The biplane max pooling is applied to.

        Returns
        -------
        :class:`torch.Tensor`
            The biplane after max pooling.
        """

        return max_pool_biplane( input, **self._max_pool_kwargs )

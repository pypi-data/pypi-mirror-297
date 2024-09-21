from typing import Optional

import torch

from .._kernel_sizes import _size_2_t


__all__ = [ 'max_pool_biplane' ]


def max_pool_biplane(
        input: torch.Tensor,
        kernel_size: _size_2_t,
        stride: Optional[_size_2_t] = None,
        padding:  _size_2_t = 0,
        dilation: _size_2_t = 1,
        return_indices: bool = False,
        ceil_mode: bool = False
) -> torch.Tensor:
    """Applies max pooling to a biplane.
    See :class:`MaxPoolBiplane` for details.
    """

    processed = torch.nn.functional.max_pool2d(
        input.flatten( end_dim = -4 ),
        kernel_size = kernel_size,
        stride = stride,
        padding = padding,
        dilation = dilation,
        return_indices = return_indices,
        ceil_mode = ceil_mode
    )

    if return_indices:
        return tuple(
            tensor.view(*input.shape[:-3], *tensor.shape[-3:])
            for tensor in processed
        )
    else:
        return processed.view(*input.shape[:-3], *processed.shape[-3:])
        

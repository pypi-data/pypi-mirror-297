import itertools as it

import torch

from ._kernel_sizes import _size_2_t, _size_3_t, _size_2_t_to_3_t


__all__ = [ 'ConvBiplane' ]


def _get_kernel_depth(input: _size_3_t) -> int:
    if type(input) is int:
        return input
    else:
        return input[0]

class ConvBiplane(torch.nn.Module):
    r"""*Biplane convolutional* neural network layer.

    A *biplane convolutional* neural network layer
    is a particular type of group equivariant neural network layer
    taking a biplane as an input
    and producing a new biplane as an output
    by applying a cross-correlation with respect to an action
    of a discretized version of the abelian group
    :math:`\Z \times \R^2`.
    Thinking of the biplane as a discretization of a function
    on :math:`\{0, 1\} \times \R^2`,
    the corresponding action
    of :math:`\Z \times \R^2` on :math:`\{0, 1\} \times \R^2`
    is

    .. math::
        \begin{aligned}
        (\Z \times \R^2) \times (\{0, 1\} \times \R^2)
        & \to
        \{0, 1\} \times \R^2,
        \\
        ((k, v), (d, p))
        & \mapsto
        T^k(d, v+p),
        \end{aligned}
    
    where

    .. math::
        \begin{aligned}
        T \colon \{0, 1\} \times \R^2
        & \to
        \{0, 1\} \times \R^2,
        \\
        (0, p)
        & \mapsto
        (1, p),
        \\
        (1, p)
        & \mapsto
        (0, p - (0, \mathrm{shift}))
        .
        \end{aligned}

    Parameters
    ----------
    in_channels : :class:`int`
        The number of channels in the input biplane.
    out_channels : :class:`int`
        The number of channels produced by the cross-correlation.
    kernel_size : class:`int | Tuple[int, int, int]`
        The size of the convolution kernel.
    shift : :class:`int`
        The :math:`\mathrm{shift}`-parameter in the definition of
        :math:`{T \colon \{0, 1\} \times \R^2 \to \{0, 1\} \times \R^2}`.
    stride : :class:`int | Tuple[int, int]`, optional
        The stride of the cross-correlation,
        defaults to :obj:`1`.
    padding : :class:`int | Tuple[int, int]`, optional
        Padding added to all four sides of the biplane,
        defaults to :obj:`0`.
    dilation : :class:`int | Tuple[int, int]`, optional
        The spacing between kernel elements,
        defaults to :obj:`1`.
    groups : :class:`int`, optional
        The number of blocked connections
        from input channels to output channels,
        defaults to :obj:`1`.
    bias : :class:`bool`, optional
        If this is set to :obj:`True`,
        then a learnable bias is added to the output,
        defaults to :obj:`True`.
    padding_mode : :class:`str`, optional
        One of the four padding modes
        :obj:`'zeros'`, :obj:`'reflect'`, :obj:`'replicate'`
        or :obj:`'circular'`,
        defaults to :obj:`'zeros'`.
    """
    
    def __init__(self,
                 in_channels: int,
                 out_channels: int,
                 kernel_size: _size_3_t,
                 *,
                 shift: int,
                 stride:   _size_2_t = 1,
                 padding:  _size_2_t = 0,
                 dilation: _size_2_t = 1,
                 groups: int = 1,
                 bias: bool = True,
                 padding_mode: str = 'zeros',
                 device = None,
                 dtype = None
                 ) -> None:

        super().__init__()

        self.conv3d = torch.nn.Conv3d(
            in_channels,
            out_channels,
            kernel_size,
            stride   = _size_2_t_to_3_t( 1, stride   ),
            padding  = _size_2_t_to_3_t( 0, padding  ),
            dilation = _size_2_t_to_3_t( 1, dilation ),
            groups = groups,
            bias = bias,
            padding_mode = padding_mode,
            device = device,
            dtype = dtype
        )
        """:class:`torch.nn.Conv3d`: The convolution module used internally."""

        self._shift = shift
        
        self._nb_biplanes, self._need_single_plane = divmod(
            _get_kernel_depth( kernel_size ) + 1,
            2
        )
        
        self._nb_padding_patches = self._nb_biplanes + self._need_single_plane
        
    def forward(self,
                input: torch.Tensor,
                /) -> torch.Tensor:
        """Applies a cross-correlation as described for :class:`ConvBiplane`.

        Parameters
        ----------
        input : :class:`torch.Tensor`
            The biplane serving as an input to the cross-correlation.

        Returns
        -------
        :class:`torch.Tensor`
            The result of the cross-correlation.
        """

        sizes_prefix = (-1,) * ( len(input.shape) - 2 )
        
        return self.conv3d(
            torch.cat(
                dim = -3,
                tensors = [
                    torch.cat(
                        dim = -2,
                        tensors = [
                            sheet.narrow(
                                dim = -2,
                                start = 0,
                                length = 1
                            ).expand(
                                *sizes_prefix,
                                i * self._shift,
                                -1
                            ),
                            sheet,
                            sheet.narrow(
                                dim = -2,
                                start = -1,
                                length = 1
                            ).expand(
                                *sizes_prefix,
                                ( self._nb_padding_patches - i ) * self._shift,
                                -1
                            )
                        ]
                    ) for
                    i, sheet in enumerate(
                        it.chain(
                            it.repeat(
                                input,
                                self._nb_biplanes
                            ),
                            it.repeat(
                                input.narrow(
                                    dim = -3,
                                    start = 0,
                                    length = 1
                                ),
                                self._need_single_plane
                            )
                        )
                    )
                ]
            )
        )

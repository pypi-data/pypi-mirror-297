from typing import Tuple
from enum import StrEnum, auto

import torch
import torch.nn.functional as F


__all__ = [ 'ReshearMode', 'Reshear' ]


class ReshearMode(StrEnum):
    """Initialization parameter and attribute to :class:`Reshear`."""
    REPLICATE = auto()
    """Replicate the pixels of the left and right most columns horizontally."""
    ZERO = auto()
    """Fill the surrounding pixels with zeros."""


class Reshear(torch.nn.Module):
    """Reshears a biplane.

    The biplanes rendered by :class:`BiplaneFromIntervals` and
    :class:`BiplaneFromTriangles` are sheared
    in comparison to the strip indexing
    the unravelled relative homology lattice
    to save on memory and computation.
    This module undoes the sheering inherents to these two classes
    and can be used for visualization purposes.

    Parameters
    ----------
    shape : :class:`torch.Size`
        The shape of the tensors to be processed.
        Only the last two components matter,
        the others are ignored.
    mode : :class:`ReshearMode`, optional
        See :class:`ReshearMode` for details.
        The corresponding attribute
        :attr:`mode` can be changed after initialization.
        The default is :obj:`ReshearMode.ZERO`.
    """
    
    def __init__(self,
                 *,
                 shape: torch.Size,
                 mode: ReshearMode = ReshearMode.ZERO,
                 device = None,
                 dtype = None
                 ) -> None:

        super().__init__()

        self.mode = mode
        """:class:`ReshearMode`: See :class:`ReshearMode` for details."""
        
        rows, columns = shape[-2:]

        indices_bottom = torch.arange(
            start = 1,
            end = columns + rows,
            dtype = torch.long,
            device = device
        )[None, :]

        offsets = torch.arange(
            start = 1 - rows,
            end = 1,
            dtype = torch.long,
            device = device
        )[:, None]

        self._indices = torch.maximum(
            torch.tensor(0, dtype=torch.long, device=device),
            torch.minimum(
                torch.tensor(columns+1, dtype=torch.long, device=device),
                offsets + indices_bottom
            )
        )

    def _pad(self,
             input: torch.Tensor,
             /) -> torch.Tensor:
        match self.mode:
            case ReshearMode.REPLICATE:
                return torch.cat(
                    dim = -1,
                    tensors = [
                        input.narrow(
                            dim = -1,
                            start = 0,
                            length = 1
                        ),
                        input,
                        input.narrow(
                            dim = -1,
                            start = -1,
                            length = 1
                        )
                    ]
                )
            case ReshearMode.ZERO:
                return F.pad(
                    input,
                    pad = (1, 1, 0, 0),
                    mode = 'constant',
                    value = 0
                )

    def forward(self,
                input: torch.Tensor,
                /) -> torch.Tensor:
        """Reshears the input.

        Parameters
        ----------
        input : :class:`torch.Tensor`
            The tensor to be resheared.

        Returns
        -------
        :class:`torch.Tensor`
            The resheared tensor.
        """
        
        return self._pad( input ).take_along_dim(
            dim = -1,
            indices = self._indices.view(
                (1,) * (len(input.shape) - 2) + self._indices.shape
            )
        )

    @classmethod
    def create_n_apply(cls,
                       input: torch.Tensor,
                       *,
                       mode: ReshearMode = ReshearMode.ZERO,
                       device = None,
                       dtype = None
                       ) -> Tuple[torch.Tensor, None]:
        """Creates a matching instance and applies it.

        This class method creates an instance
        with the :obj:`shape` parameter matching the :obj:`input`
        and applies it to :obj:`input`.
        Both the processed input tensor
        as well as the instance are returned.

        Parameters
        ----------
        input : :class:`torch.Tensor`
            The tensor to be resheared.
        mode : :class:`ReshearMode`, optional
            See :class:`ReshearMode` for details.
            The corresponding attribute
            :attr:`mode` can be changed after initialization.
            The default is :obj:`ReshearMode.ZERO`.

        Returns
        -------
        :class:`Tuple[torch.Tensor, Reshear]`
            Pair with the first component containing the sheared tensor
            and the second component the instance that was used to create it.
        """
        
        instance = cls(
            shape = input.shape,
            mode = mode,
            device = device,
            dtype = dtype
        )
        return ( instance(input), instance )
    

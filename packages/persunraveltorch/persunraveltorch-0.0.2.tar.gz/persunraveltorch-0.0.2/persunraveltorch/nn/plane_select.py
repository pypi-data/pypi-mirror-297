import torch

from .functional import plane_select


__all__ = [ 'PlaneSelect' ]


class PlaneSelect(torch.nn.Module):
    """Selects one of the planes in a biplane.

    This module takes a biplane as an input
    and outputs one of the two planes.

    Parameters
    ----------
    plane : :class:`int`
        The index of the plane to select,
        which can be :obj:`0` or :obj:`1`.
        The corresponding attribute :attr:`plane`
        can be changed after initialization.
    """
    
    def __init__(self,
                 plane: int # should be 0 or 1 when processing biplanes
                 ) -> None:

        super().__init__()

        self.plane = plane
        """:class:`int`: The index of the plane to select."""
        
    def forward(self,
                input: torch.Tensor,
                /) -> torch.Tensor:
        """Selects the plane with index :attr:`plane`.

        Parameters
        ----------
        input : :class:`torch.Tensor`
            The biplane to process.
        
        Returns
        -------
        :class:`torch.Tensor`
            The selected plane.
        """

        return plane_select( input, plane = self.plane )

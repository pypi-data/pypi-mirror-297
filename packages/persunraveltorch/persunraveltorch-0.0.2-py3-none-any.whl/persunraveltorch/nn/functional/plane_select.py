import torch

__all__ = [ 'plane_select' ]

def plane_select(
        input: torch.Tensor,
        plane: int # should be 0 or 1 when input is a biplane
        ) -> torch.Tensor:
    """Selects one of the planes in a biplane.
    See :class:`PlaneSelect` for details.
    """
    return input.narrow(
        dim = -3,
        start = plane,
        length = 1
    ).squeeze( dim = -3 )

import torch
import torch.nn as nn


__all__ = [ 'StripAffineFunctional' ]


class StripAffineFunctional(nn.Module):
    """Affine functional induced by a sheared bitmap and a bias.

    The affine functional on sheared bitmaps
    induced by a single sheared bitmap as a weight and a bias.

    Parameters
    ----------
    weight : :class:`torch.Tensor`
        The sheared bitmap used as a weight.
    bias : :class:`torch.Tensor`
        The singleton tensor used as a bias.
    pixel_area : float
        The area covered by each pixel.
    """

    def __init__(self,
                 weight: torch.Tensor,
                 bias: torch.Tensor,
                 pixel_area: float
                 ) -> None:
        super().__init__()
        self.weight = nn.Parameter( weight )
        """:class:`nn.Parameter`: The sheared bitmap used as a weight."""
        self.bias   = nn.Parameter( bias   )
        """:class:`nn.Parameter`: The singleton parameter used as a bias."""
        self.pixel_area = pixel_area
        """:class:`float`: The area covered by each pixel."""

    def forward(self,
                input: torch.Tensor
                ) -> torch.Tensor:
        """Applies the affine functional to the input.

        Parameters
        ----------
        input : :class:`torch.Tensor`
            The sheared bitmap passed as an argument to the affine functional.

        Returns
        -------
        :class:`torch.Tensor`
            The singleton tensor obtained as a result.
        """
        return (
            input * self.weight * self.pixel_area
        ).sum( dim = (1, 2) ) + self.bias

    def energy(self) -> torch.Tensor:
        """:class:`torch.Tensor`: The energy of the weight."""
        return ( self.weight.pow(2) * self.pixel_area ).sum()

    def variational_energy(self) -> torch.Tensor:
        """:class:`torch.Tensor`: The energy of the gradient of the weight."""
        partial_x = self.weight[:,1:] - self.weight[:,:-1]
        partial_y = self.weight[:-1,:-1] - self.weight[1:,1:]
        return partial_x.pow(2).sum() + partial_y.pow(2).sum()

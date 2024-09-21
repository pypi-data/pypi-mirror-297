from typing import Optional
from importlib import import_module
import torch
import torch.nn as nn
import torch.nn.functional as F

from . import Reshear, ReshearMode

__all__ = [ 'StripAffineFunctional' ]


def try_to_import_plt():
    try:
        return import_module( "matplotlib.pyplot" )
    except ModuleNotFoundError:
        return None

plt = try_to_import_plt()


class StripAffineFunctional(nn.Module):

    def __init__(self,
                 weight: torch.Tensor,
                 bias: torch.Tensor,
                 pixel_area: torch.Tensor,
                 padding: int = 0
                 ) -> None:
        super().__init__()
        # self._padding = padding
        self._reshear = Reshear(
            shape = weight.shape#,
            # mode = ReshearMode.REPLICATE
        )
        self.weight = nn.Parameter(
            self._reshear( weight )
        )
        self.bias   = nn.Parameter( bias )
        self.pixel_area = pixel_area


    def forward(self,
                input: torch.Tensor
                ) -> torch.Tensor:
        # padding = self._padding
        return (
            self._reshear( input ) * self.weight * self.pixel_area
        ).sum( dim = (1, 2) ) + self.bias

    def energy(self) -> torch.Tensor:
        return ( self.weight.pow(2) * self.pixel_area ).sum()

    def variational_energy(self) -> torch.Tensor:
        partial_x = self.weight[:,1:] - self.weight[:,:-1]
        partial_y = self.weight[:-1] - self.weight[1:]
        return partial_x.pow(2).sum() + partial_y.pow(2).sum()

    def viz_normal(self):
        if plt is None:
            raise ModuleNotFoundError(
                "The method 'viz_normal' requires 'matplotlib' as a dependency"
            )
        fig, ax = plt.subplots(figsize=(15,12))
        
        ax.axis('off')
        ax.matshow( self.weight.detach().numpy() )

        return fig
        

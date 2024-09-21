from typing import Optional

import torch

class GlueToFragment(torch.nn.Module):

    def __init__(self,
                 *,
                 pixel_columns: int,
                 padding: int,
                 max_overhead: Optional[int] = None,
                 device = None
                 ) -> None:

        super().__init__()

        self.max_overhead = max_overhead
        
        self._pad = torch.nn.ZeroPad1d(padding)

        # Create indices
        
        indices_bottom = torch.arange(
            start = 0,
            end = pixel_columns + 2 * padding,
            dtype = torch.long,
            device = device
        )[None, :]

        offsets = torch.arange(
            start = pixel_columns - 1,
            end = -1,
            step = -1,
            dtype = torch.long,
            device = device
        )[:, None]

        self._indices = offsets + indices_bottom
        
    def forward(self,
                triangle01: torch.Tensor,
                triangle02: torch.Tensor,
                /) -> torch.Tensor:

        triangle02_transformed = triangle02.flip( dims = (-1, -2) ).transpose(
            dim0 = -1,
            dim1 = -2
        )

        unsheared_fragment = self._pad(
            torch.cat(
                ( triangle02_transformed, triangle01 ),
                dim = -1
            )
        )

        if self.max_overhead is None:
            return unsheared_fragment.take_along_dim(
                dim = -1,
                indices = self._indices.view(
                    (1,) * (len(triangle01.shape) - 2) + self._indices.shape
                )
            )

        unsheared_fragment_flattened = unsheared_fragment.flatten(
            end_dim = -3
        )

        split_size = max(
            1,
            self.max_overhead // (
                unsheared_fragment_flattened.shape[0] *
                self._indices.nelement() *
                self._indices.element_size()
            )
        )

        return torch.cat(
            [ unsheared_fragment_piece.take_along_dim(
                self._indices[None, :, :], dim = -1) for
              unsheared_fragment_piece in torch.split(
                  unsheared_fragment_flattened,
                  split_size)
            ]
        ).view(*unsheared_fragment.shape[:-2], *self._indices.shape)

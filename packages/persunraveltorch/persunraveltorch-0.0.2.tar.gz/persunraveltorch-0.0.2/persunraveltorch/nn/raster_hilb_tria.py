from math import pi
import torch

class RasterHilbTria(torch.nn.Module):

    def __init__(self,
                 pixel_columns: int,
                 *,
                 range_intervals: tuple(float, float) = (0.0, pi/2.0),
                 device = None,
                 dtype = None
                 ) -> None:

        super().__init__()

        min, max = range_intervals

        self._strip_width = max - min
        self._side_len = self._strip_width / pixel_columns
        self._pixel_area = self._side_len * self._side_len

        self._px = torch.linspace(
            start = min,
            end = max - self._side_len,
            steps = pixel_columns,
            dtype = dtype,
            device = device
        )[None, :, None]

        self._py = torch.linspace(
            start = max,
            end = min + self._side_len,
            steps = pixel_columns,
            dtype = dtype,
            device = device
        )[:, None, None]

    def forward(self,
                intervals00: torch.Tensor,
                intervals01: torch.Tensor,
                /) -> torch.Tensor:

        a0_unsqueezed, b0_unsqueezed = intervals00.split( 1, dim = -1 )

        a1_unsqueezed, b1_unsqueezed = intervals01.split( 1, dim = -1 )
        
        a0 = a0_unsqueezed.squeeze( dim = -1 )
        b0 = b0_unsqueezed.squeeze( dim = -1 )
        a1 = a1_unsqueezed.squeeze( dim = -1 )
        b1 = b1_unsqueezed.squeeze( dim = -1 )

        x = torch.cat(
            ( a0, b1 - self._strip_width ),
            dim = -1
        ).unsqueeze(dim=-2).unsqueeze(dim=-2)

        y = torch.cat(
            ( b0, a1 ),
            dim = -1
        ).unsqueeze(dim=-2).unsqueeze(dim=-2)

        hor_seg = torch.maximum(
            0,
            torch.minimum(
                self._side_len,
                torch.minimum(
                    self._px + self._side_len - x,
                    y - self._px
                )
            )
        )

        vert_seg = torch.maximum(
            0,
            torch.minimum(
                self._side_len,
                torch.minimum(
                    self._py + self._side_len - y,
                    x + self._strip_width - self._py
                )
            )
        )

        return (
            hor_seg.unsqueeze(-2) @ vert_seg.unsqueeze(-1)
        ).squeeze( (-2, -1) ) / self._pixel_area


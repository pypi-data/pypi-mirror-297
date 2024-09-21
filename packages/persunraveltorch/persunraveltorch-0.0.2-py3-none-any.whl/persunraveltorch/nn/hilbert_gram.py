from collections.abc import Sequence
import torch

from .hilbert_kernel import HilbertKernel


__all__ = [ 'HilbertGram' ]


class HilbertGram(HilbertKernel):
    r"""As :class:`HilbertKernel`
    but for different sizes in dimension :obj:`-3`.

    If the first input consists of tensors
    of shape :math:`([\dots,] m, k, 2)`
    for some :math:`{m \in \N}`
    and the second input consists of tensors
    of shape :math:`([\dots,] n, k, 2)`
    for some :math:`{n \in \N}`,
    then the output has shape :math:`([\dots,] m, n)`
    containing all results of pairwise kernel computations
    as a Gram matrix.
    Parameters and attributes are inherited from :class:`HilbertKernel`.
    """

    def forward(self,
                intervals01: Sequence[torch.Tensor],
                intervals02: Sequence[torch.Tensor],
                /) -> torch.Tensor:
        """Computes the Gram matrix of the corresponding Hilbert functions.

        Parameters
        ----------
        intervals01 : :class:`Sequence[torch.Tensor]`
            Persistence intervals
            for the first input
            as a :class:`Sequence[torch.Tensor]` by degree.
            Each item of this sequence
            is a :class:`torch.Tensor` of shape
            :math:`([\dots,] m, k, 2)`,
            where :math:`k` is the number of persistence intervals
            in the corresponding degree.
        intervals02 : :class:`Sequence[torch.Tensor]`
            Persistence intervals
            for the second input
            as a :class:`Sequence[torch.Tensor]` by degree.
            Each item of this sequence
            is a :class:`torch.Tensor` of shape
            :math:`([\dots,] n, k, 2)`,
            where :math:`k` is the number of persistence intervals
            in the corresponding degree.

        Returns
        -------
        :class:`torch.Tensor`
            The Gram matrix of the corresponding Hilbert functions.
        """
        
        return super().forward(
            [ intervals_sd.unsqueeze(-3) for intervals_sd in intervals01 ],
            [ intervals_sd.unsqueeze(-4) for intervals_sd in intervals02 ]
        )

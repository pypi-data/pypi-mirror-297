from typing import Tuple

_size_2_t = int | Tuple[     int, int]
_size_3_t = int | Tuple[int, int, int]

def _size_2_t_to_3_t(
        fill_val: int,
        input: _size_2_t) -> _size_3_t:
    if type(input) is int:
        return (fill_val, input, input)
    else:
        return (fill_val,) + input

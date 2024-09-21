from enum import StrEnum, auto
from dataclasses import dataclass
from typing import Optional, NamedTuple


__all__ = [ 'Unit', 'Length', 'Sizes' ]


class Unit(StrEnum):
    EM = auto()
    EX = auto()
    PX = auto()
    IN = auto()
    CM = auto()
    MM = auto()
    PT = auto()
    PC = auto()
    PERCENT = '%'

    
class Length(NamedTuple):
    value: float
    unit: Unit

    def __str__(self):
        return f"{self.value}{self.unit}"

    
@dataclass(frozen=True, slots=True)
class Sizes:
    width:  Optional[Length] = None
    height: Optional[Length] = None

    def __str__(self):
        return " ".join(
            ([f'width="{self.width}"'  ] if self.width  is not None else []) +
            ([f'height="{self.height}"'] if self.height is not None else [])
        )

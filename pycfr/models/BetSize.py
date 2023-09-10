from dataclasses import dataclass
from enum import StrEnum


class BetSizeType(StrEnum):
    """Represents bet size types.

    Attributes:
        PotRelative: ...
        PrevBetRelative: ...
        Additive: ...
        Geometric: ...
        AllIn: ...
    """

    PotRelative: str = "PotRelative"
    PrevBetRelative: str = "PrevBetRelative"
    Additive: str = "Additive"
    Geometric: str = "Geometric"
    AllIn: str = "AllIn"


@dataclass
class BetSize:
    """Represents a bet size in a game.

    Attributes:
        type (BetSizeType): The type of bet size (PotRelative, PrevBetRelative,
            Additive, Geometric, or AllIn).
        value (int | float | tuple[int, float] | None): The value of the bet size.


    Example:
        >>> BetSize(BetSizeType.AllIn)
        >>> BetSize(BetSizeType.AllIn)
        BetSize(type=<BetSizeType.AllIn: 'AllIn'>, value=None)

    """

    type: BetSizeType
    value: int | float | tuple[int, float]

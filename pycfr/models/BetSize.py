from dataclasses import dataclass
from enum import StrEnum


class BetSizeType(StrEnum):
    """Represents bet size types.

    Attributes:
        PotRelative: pass.
        PrevBetRelative: pass.
        Additive: pass.
        Geometric: pass.
        AllIn: pass.
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
        >>> BetSize(BetSizeType.PotRelative, 20)
        BetSize(type=<BetSizeType.PotRelative: 'PotRelative'>, value=20)
        >>> bet_size = BetSize(BetSizeType.PotRelative, 20)
        >>> bet_size.type
        <BetSizeType.PotRelative: 'PotRelative'>
        >>> bet_size.type == "PotRelative"
        True
        >>> bet_size.type == BetSizeType.PotRelative
        True
        >>> bet_size.value
        20

    """

    type: BetSizeType
    value: int | float | tuple[int, float]

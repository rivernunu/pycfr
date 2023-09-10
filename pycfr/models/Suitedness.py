from dataclasses import dataclass
from enum import StrEnum


class SuitednessType(StrEnum):
    """An enumeration representing different types of suits in a game.

    Attributes:
        Suited (str): Represents a suited suit type.
        Offsuit (str): Represents an offsuit suit type.
        All (str): Represents all suit types.
        Specific (str): Represents a specific suit type.

    Example:
        >>> SuitednessType.Suited
        <SuitednessType.Suited: 'Suited'>
        >>> print(SuitednessType.Suited)
        Suited
    """

    Suited: str = "Suited"
    Offsuit: str = "Offsuit"
    All: str = "All"
    Specific: str = "Specific"


@dataclass
class Suitedness:
    """Represents the suitedness of a hand in a game.

    Attributes:
        type (SuitednessType): The type of suitedness (Suited, Offsuit, All, or Specific).
        suit (tuple[int, int] | None): The value of the specif suitedness.

    Example:
        >>> Suitedness(SuitednessType.Suited)
        Suitedness(type=<SuitednessType.Suited: 'Suited'>, suit=None)
        >>> Suitedness(SuitednessType.Specific, (0,1))
        Suitedness(type=<SuitednessType.Specific: 'Specific'>, suit=(0, 1))
    """

    type: SuitednessType
    suit: tuple[int, int] | None = None

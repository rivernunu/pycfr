from dataclasses import dataclass


@dataclass
class Suitedness:
    Suited: bool = False
    Offsuit: bool = False
    All: bool = False
    Specific: tuple[int, int] = (-1, -1)

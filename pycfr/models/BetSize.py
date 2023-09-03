from dataclasses import dataclass


@dataclass
class BetSize:
    PotRelative: float
    PrevBetRelative: float
    Additive: int
    Geometric: tuple[int, int]
    Allin: str

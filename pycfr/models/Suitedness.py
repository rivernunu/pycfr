from dataclasses import dataclass


@dataclass
class Suitedness:
    Suited: bool = False
    Offsuit: bool = False
    All: bool = False
    Specific: bool = False
    suit1: int = -1
    suit2: int = -1

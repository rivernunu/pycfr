from dataclasses import dataclass


@dataclass
class Suitedness:
    Suited: str = ""
    Offsuit: str = ""
    All: str = ""
    Specific: list[int, int] = [-1, -1]

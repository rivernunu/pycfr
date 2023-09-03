from dataclasses import dataclass

from models.BetSize import BetSize


@dataclass
class BetSizeCandidates:
    bet: list[BetSize]
    raise_: list[BetSize]

from dataclasses import dataclass

from constants import NOT_DEALT
from models.Range import Range


@dataclass
class CardConfig:
    range_: tuple[Range]
    flop: list[int] = [NOT_DEALT, NOT_DEALT, NOT_DEALT]
    turn: int = NOT_DEALT
    river: int = NOT_DEALT

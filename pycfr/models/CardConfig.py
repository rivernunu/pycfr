from dataclasses import dataclass, field

from pycfr.constants import NOT_DEALT
from pycfr.models.Range import Range


@dataclass
class CardConfig:
    """Represents the configuration of cards in a game.

    Attributes:
        each_range (tuple[Range, Range]): A tuple representing the range of cards for each player.
        flop (list[int]): A list representing the flop cards.
        turn (list[int]): A list representing the turn card.
        river (list[int]): A list representing the river card.
    """

    each_range: tuple[Range, Range]
    flop: list[int] = field(default_factory=lambda: [NOT_DEALT] * 3)
    turn: list[int] = field(default_factory=lambda: [NOT_DEALT])
    river: list[int] = field(default_factory=lambda: [NOT_DEALT])

"""Tree Config.

Example:
>>> bet_sizes = BetSizeStrategy(bet_str="60%,e,a", raise_str="2.5x")
>>> tree_config = TreeConfig(
...     initial_state=BoardState.Flop,
...     starting_pot=200,
...     effective_stack=[100, 100],
...     rake_rate=0.0,
...     rake_cap=0.0,
...     flop_bet_sizes=[bet_sizes, bet_sizes],
...     turn_bet_sizes=[bet_sizes, bet_sizes],
...     river_bet_sizes=[bet_sizes, bet_sizes],
...     turn_donk_sizes=[],
...     river_donk_sizes=[],
...     add_allin_threshold=1.5,
...     force_allin_threshold=0.15,
...     merging_threshold=0.1
... )

"""

from dataclasses import dataclass

from pycfr.models.BetSizeStrategy import BetSizeStrategy
from pycfr.models.DonkSizeStrategy import DonkSizeStrategy
from pycfr.models.BoardState import BoardState


@dataclass
class TreeConfig:
    """_summary_.

    Attributes:
        initial_state (BoardState): represents flop, turn, or river.
        starting_pot (int): initial pot size. must be greater than 0.
        effective_stack (list[int]): pass.

    """

    initial_state: BoardState
    starting_pot: int
    effective_stack: list[int]
    rake_rate: float
    rake_cap: float
    flop_bet_sizes: list[BetSizeStrategy]
    turn_bet_sizes: list[BetSizeStrategy]
    river_bet_sizes: list[BetSizeStrategy]
    turn_donk_sizes: DonkSizeStrategy | None
    river_donk_sizes: DonkSizeStrategy | None
    add_allin_threshold: float
    force_allin_threshold: float
    merging_threshold: float

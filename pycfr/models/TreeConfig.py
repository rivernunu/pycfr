from dataclasses import dataclass

from pycfr.models.BetSizeStrategy import BetSizeStrategy
from pycfr.models.BoardState import BoardState


@dataclass
class TreeConfig:
    initial_state: BoardState
    starting_pot: int
    effective_stack: int
    rake_rate: float
    rake_cap: float
    flop_bet_sizes: list[BetSizeStrategy]
    turn_bet_sizes: list[BetSizeStrategy]
    river_bet_sizes: list[BetSizeStrategy]
    turn_donk_sizes: list[BetSizeStrategy]
    river_donk_sizes: list[BetSizeStrategy]
    add_allin_threshold: float
    force_allin_threshold: float
    merging_threshold: float

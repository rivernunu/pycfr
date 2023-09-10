from dataclasses import dataclass, field
from typing import Optional

from pycfr.constants import (NOT_DEALT, PLAYER_CHANCE_FLAG, PLAYER_MASK_FLAG,
                             PLAYER_OOP, PLAYER_TERMINAL_FLAG)
from pycfr.models.Action import Action


@dataclass
class Node:
    prev_action: Action
    player: int = PLAYER_OOP
    turn: int = NOT_DEALT
    river: int = NOT_DEALT
    is_locked: bool = False
    amount: int = 0
    children_offset: int = 0
    num_children: int = 0
    num_elements_ip: int = 0
    num_elements: int = 0
    scale1: float = 0.0
    scale2: float = 0.0
    scale3: float = 0.0
    storage1: bytearray = field(default_factory=bytearray)
    storage2: bytearray = field(default_factory=bytearray)
    storage3: bytearray = field(default_factory=bytearray)

    def is_terminal(self) -> bool:
        """終端かどうかを返す.

        Returns:
            bool: 終端のときTrue, そうでなければFalse.
        """
        if self.player & PLAYER_TERMINAL_FLAG == 0:
            return False
        else:
            return True

    def is_chance(self) -> bool:
        if self.player & PLAYER_CHANCE_FLAG == 0:
            return False
        else:
            return True

    def cfvalue_storage_player(self) -> Optional[int]:
        prev_player = self.player & PLAYER_MASK_FLAG
        if prev_player == 0:
            return 1
        elif prev_player == 1:
            return 0
        else:
            return None

from dataclasses import dataclass
from typing import Self

from pycfr.models.Action import Action
from pycfr.models.BoardState import BoardState


@dataclass
class ActionTreeNode:
    player: int
    board_state: BoardState
    amount: int
    actions: list[Action]
    children: list[Self]

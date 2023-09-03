from dataclasses import dataclass
from typing import Self

from models.Action import Action
from models.BoardState import BoardState


@dataclass
class ActionTreeNode:
    player: int
    board_state: BoardState
    amount: int
    actions: list[Action]
    children: list[Self]

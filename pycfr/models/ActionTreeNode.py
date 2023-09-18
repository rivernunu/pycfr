from dataclasses import dataclass

from pycfr.constants import PLAYER_CHANCE_FLAG, PLAYER_TERMINAL_FLAG
from pycfr.models.Action import Action
from pycfr.models.BoardState import BoardState


@dataclass
class ActionTreeNode:
    """_summary_.

    Attributes:
        player (int): 0, 1.
        board_state (BoardState): flop, turn, river.
        amount (int): pass.
        actions (list[Action]): pass.
        children (list["ActionTreeNode]): pass.

    """

    player: int
    board_state: BoardState
    amount: int
    actions: list[Action]
    children: list["ActionTreeNode"]

    def __init__(
        self,
        board_state: BoardState,
        player: int = 0,
        amount: int = 0,
        actions: list[Action] = [],
        children: list["ActionTreeNode"] = [],
    ):
        self.player = player
        self.board_state = board_state
        self.amount = amount
        self.actions = actions
        self.children = children

    def is_terminal(self) -> bool:
        return self.player & PLAYER_TERMINAL_FLAG != 0

    def is_chance(self) -> bool:
        return self.player & PLAYER_CHANCE_FLAG != 0

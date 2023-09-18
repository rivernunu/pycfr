from dataclasses import dataclass

from pycfr.constants import PLAYER_OOP
from pycfr.models.Action import Action, ActionType


@dataclass
class GameBuildTreeInfo:
    flop_idx: int
    turn_idx: int
    river_idx: int
    num_storage: int
    num_storage_ip: int
    num_storage_chance: int


@dataclass
class ActionBuildTreeInfo:
    """_summary_.

    Attributes:
        prev_action (Action): pass.
        num_bets (int): pass.
        oop_call_flag (bool): pass.
        stack (list[int)]): pass.
        prev_amount (int): pass.

    Raises:
        ValueError: _description_

    Example:
        >>> ActionBuildTreeInfo(player )

    Hierarchy:
        Game.update_config --> ActionTree.invalid_terminal
        -- > ActionTree.invalid_terminals_recursive --> ActionBuildTreeInfo

        ActionTree.add_action --> ActionTree.add_line
        --> ActionTree.add_line_recursive --> ActionBuildTreeInfo

    """

    prev_action: Action
    num_bets: int
    allin_flag: bool
    oop_call_flag: bool
    stack: list[int]
    prev_amount: int

    def __init__(
        self,
        prev_action: Action = Action(ActionType.Nothing, value=None),
        num_bets: int = 0,
        allin_flag: bool = False,
        oop_call_flag: bool = False,
        stack: list[int] = [0, 0],
        prev_amount: int = 0,
    ) -> None:
        self.prev_action = prev_action
        self.num_bets = num_bets
        self.allin_flag = allin_flag
        self.oop_call_flag = oop_call_flag
        self.stack = stack
        self.prev_amount = prev_amount

    def __post_init__(self) -> None:
        if self.stack == [0, 0]:
            raise ValueError(f"stack must be larger than 0. {self.stack}")

    def create_next(self, player: int, action: Action) -> "ActionBuildTreeInfo":
        """_summary_.

        Args:
            player (int): an integer representing the player (OOP or IP)
            action (Action): an enum representing the action performed by player.
            (Fold, Check, Call, Bet, Raise, AllIn, or Chance.)

        Returns:
            Self: _description_

        Hierarchy:
            ActionTree._build_tree_recursive --> create_next
            ActionTree._add_line_recursive --> create_next
            ActionTree._total_bet_amount_recursive --> create_next
        """
        num_bets = self.num_bets
        allin_flag = self.allin_flag
        oop_call_flag = self.oop_call_flag
        stack = self.stack.copy()
        prev_amount = self.prev_amount

        if action.type == ActionType.Check:
            oop_call_flag = False
        elif action.type == ActionType.Call:
            num_bets = 0
            oop_call_flag = player == PLAYER_OOP
            stack[player] = stack[player ^ 1]
            prev_amount = 0
        elif action.type in [ActionType.Bet, ActionType.Raise, ActionType.AllIn]:
            to_call = stack[player] - stack[player ^ 1]
            num_bets += 1
            allin_flag = action.type == ActionType.AllIn
            if action.value is None:
                raise ValueError
            stack[player] -= action.value - prev_amount + to_call
            prev_amount = action.value

        action_build_tree_info = ActionBuildTreeInfo(
            action,
            num_bets,
            allin_flag,
            oop_call_flag,
            stack,
            prev_amount,
        )

        return action_build_tree_info

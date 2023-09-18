from dataclasses import dataclass
from enum import StrEnum


class ActionType(StrEnum):
    """An enumeration representing different types of actions in a game.

    Attributes:
        Nothing (str): Represents taking no action.
        Fold (str): Represents folding.
        Check (str): Represents checking.
        Call (str): Represents calling.
        Bet (str): Represents betting.
        Raise (str): Represents raising.
        AllIn (str): Represents going all-in.
        Chance (str): Represents taking a chance or making a risky move.

    Example:
        >>> ActionType.Raise
        <ActionType.Raise: 'Raise'>
        >>> print(ActionType.Raise)
        Raise
    """

    Nothing: str = "Nothing"
    Fold: str = "Fold"
    Check: str = "Check"
    Call: str = "Call"
    Bet: str = "Bet"
    Raise: str = "Raise"
    AllIn: str = "AllIn"
    Chance: str = "Chance"


@dataclass
class Action:
    """Action.

    Attribute:
        type (ActionType): Nothing, Fold, Check, Call, Bet, Raise, AllIn, Chance.
        value (int | None): pass.

    Example:
        >>> action = Action(ActionType.Chance, value = 0)
    """

    type: ActionType
    value: int | None

from dataclasses import dataclass

from pycfr.models.ActionType import ActionType


@dataclass
class Action:
    type: ActionType
    value: int | float | None

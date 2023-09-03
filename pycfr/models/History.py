from dataclasses import dataclass

from models.Action import Action


@dataclass
class History:
    data: list[Action]

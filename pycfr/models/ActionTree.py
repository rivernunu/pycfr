from dataclasses import dataclass

from models.Action import Action
from models.ActionTreeNode import ActionTreeNode
from models.TreeConfig import TreeConfig


@dataclass
class ActionTree:
    config: TreeConfig
    added_lines: list[list[Action]]
    removed_lines: list[list[Action]]
    root: list[ActionTreeNode]
    history: list[Action]

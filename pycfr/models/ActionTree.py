from dataclasses import dataclass, field

from pycfr.models.Action import Action
from pycfr.models.ActionTreeNode import ActionTreeNode
from pycfr.models.TreeConfig import TreeConfig


@dataclass
class ActionTree:
    config: TreeConfig
    added_lines: list[list[Action]] = field(default_factory=list)
    removed_lines: list[list[Action]] = field(default_factory=list)
    root: list[ActionTreeNode] = field(default_factory=list)
    history: list[Action] = field(default_factory=list)

    def __init__(self, config: TreeConfig) -> None:
        self.check_config(config)

    def check_config(self, config: TreeConfig) -> None:
        if config.starting_pot <= 0:
            raise ValueError

        if config.effective_stack <= 0:
            raise ValueError

        if config.rake_rate < 0.0:
            raise ValueError

        if config.rake_rate > 1.0:
            raise ValueError

        if config.rake_cap < 0.0:
            raise ValueError

        if config.add_allin_threshold < 0.0:
            raise ValueError

        if config.force_allin_threshold < 0.0:
            raise ValueError

        if config.merging_threshold < 0.0:
            raise ValueError

    def build_tree(self) -> None:
        ...

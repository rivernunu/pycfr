from dataclasses import dataclass, field

from pycfr.models.Action import Action
from pycfr.models.ActionTree import ActionTree
from pycfr.models.ActionTreeNode import ActionTreeNode
from pycfr.models.BoardState import BoardState
from pycfr.models.CardConfig import CardConfig
from pycfr.models.Node import Node
from pycfr.models.State import State
from pycfr.models.StrengthItem import StrengthItem
from pycfr.models.SwapList import SwapList
from pycfr.models.TreeConfig import TreeConfig


@dataclass
class Game:
    state: State
    # postflop game configuration
    card_config: CardConfig
    tree_config: TreeConfig
    added_lines: list[list[Action]] = field(default_factory=list)
    removed_lines: list[list[Action]] = field(default_factory=list)
    action_root: list[ActionTreeNode] = field(default_factory=list)
    # computed from configurations
    num_combinations: float = 0.0
    initial_weights: list[float] = field(default_factory=list)
    private_cards: list[int] = field(default_factory=list)
    same_hand_index: list[int] = field(default_factory=list)
    valid_indices_flop: list[int] = field(default_factory=list)
    valid_indices_turn: list[int] = field(default_factory=list)
    valid_indices_river: list[int] = field(default_factory=list)
    hand_strength: list[list[StrengthItem]] = field(default_factory=list)
    isomorphism_ref_turn: list[int] = field(default_factory=list)
    isomorphism_card_turn: list[int] = field(default_factory=list)
    isomorphism_swap_turn: list[SwapList] = field(default_factory=list)
    isomorphism_ref_river: list[int] = field(default_factory=list)
    isomorphism_card_river: list[int] = field(default_factory=list)
    isomorphism_swap_river: list[SwapList] = field(default_factory=list)
    # store options
    storage_mode: field(default_factory=BoardState)
    target_storage_mode: BoardState
    num_nodes: list[int] = field(default_factory=list)
    is_compression_enabled: bool
    num_storage: int
    num_storage_ip: int
    num_storage_chance: int
    misc_memory_usage: int
    # global storage
    node_arena: list[Node] = field(default_factory=list)
    storage1: list[int] = field(default_factory=list)
    storage2: list[int] = field(default_factory=list)
    storage_ip: list[int] = field(default_factory=list)
    storage_chance: list[int] = field(default_factory=list)
    locking_strategy: dict[int, list[float]]
    # result interpreter
    action_history: list[int] = field(default_factory=list)
    node_history: list[int] = field(default_factory=list)
    is_normalized_weight_cached: bool
    turn: int
    river: int
    turn_swapped_suit: tuple[int, int] | None
    turn_swap: int | None
    river_swap: tuple[int, int] | None
    total_bet_amount: int
    weights: list[int] = field(default_factory=list)
    normalized_weights: list[int] = field(default_factory=list)
    cfvalues_cache: list[int] = field(default_factory=list)

    def __init__(self, card_config: CardConfig, action_tree: ActionTree) -> None:
        self.update_config(card_config, action_tree)

    def update_config(self, card_config: CardConfig, action_tree: ActionTree) -> None:
        ...

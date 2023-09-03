from dataclasses import dataclass

from models.Action import Action
from models.ActionTree import ActionTree
from models.ActionTreeNode import ActionTreeNode
from models.BoardState import BoardState
from models.CardConfig import CardConfig
from models.Node import Node
from models.State import State
from models.StrengthItem import StrengthItem
from models.SwapList import SwapList
from models.TreeConfig import TreeConfig


@dataclass
class Game:
    state: State
    # postflop game configuration
    card_config: CardConfig
    tree_config: TreeConfig
    added_lines: list[list[Action]]
    removed_lines: list[list[Action]]
    action_root: list[ActionTreeNode]
    # computed from configurations
    num_combinations: float
    initial_weights: list[float]
    private_cards: list[int]
    same_hand_index: list[int]
    valid_indices_flop: list[int]
    valid_indices_turn: list[int]
    valid_indices_river: list[int]
    hand_strength: list[list[StrengthItem]]
    isomorphism_ref_turn: list[int]
    isomorphism_card_turn: list[int]
    isomorphism_swap_turn: list[SwapList]
    isomorphism_ref_river: list[int]
    isomorphism_card_river: list[int]
    isomorphism_swap_river: list[SwapList]
    # store options
    storage_mode: BoardState
    target_storage_mode: BoardState
    num_nodes: list[int]
    is_compression_enabled: bool
    num_storage: int
    num_storage_ip: int
    num_storage_chance: int
    misc_memory_usage: int
    # global storage
    node_arena: list[Node]
    storage1: list[int]
    storage2: list[int]
    storage_ip: list[int]
    storage_chance: list[int]
    locking_strategy: dict[int, list[float]]
    # result interpreter
    action_history: list[int]
    node_history: list[int]
    is_normalized_weight_cached: bool
    turn: int
    river: int
    turn_swapped_suit: tuple[int, int] | None
    turn_swap: int | None
    river_swap: tuple[int, int] | None
    total_bet_amount: int
    weights: list[int]
    normalized_weights: list[int]
    cfvalues_cache: list[int]

    def wight_config(self, card_config: CardConfig, action_tree: ActionTree) -> None:
        ...

    def update_config(self, card_config: CardConfig, action_tree: ActionTree) -> None:
        ...

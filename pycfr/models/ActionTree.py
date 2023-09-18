"""Build Action Trees.

Example:
>>> bet_sizes = BetSizeStrategy(bet_str="60%,e,a", raise_str="2.5x")
>>> donk_sizes = DonkSizeStrategy(bet_str="50%")
>>> tree_config = TreeConfig(
...     initial_state=BoardState.Turn,
...     starting_pot=200,
...     effective_stack=[900, 900],
...     rake_rate=0.0,
...     rake_cap=0.0,
...     flop_bet_sizes=[bet_sizes, bet_sizes],
...     turn_bet_sizes=[bet_sizes, bet_sizes],
...     river_bet_sizes=[bet_sizes, bet_sizes],
...     turn_donk_sizes=None,
...     river_donk_sizes=donk_sizes,
...     add_allin_threshold=1.5,
...     force_allin_threshold=0.15,
...     merging_threshold=0.1
... )
>>> action_tree = ActionTree(config=tree_config)
>>> print(action_tree)


"""
from collections import namedtuple
from dataclasses import dataclass, field

from pycfr.constants import (
    PLAYER_CHANCE,
    PLAYER_CHANCE_FLAG,
    PLAYER_OOP,
    PLAYER_TERMINAL_FLAG,
    PLAYER_FOLD_FLAG,
)
from pycfr.models.Action import Action, ActionType
from pycfr.models.ActionTreeNode import ActionTreeNode
from pycfr.models.BetSize import BetSizeType, BetSize
from pycfr.models.BetSizeStrategy import BetSizeStrategy
from pycfr.models.DonkSizeStrategy import DonkSizeStrategy
from pycfr.models.BoardState import BoardState
from pycfr.models.BuildTreeInfo import ActionBuildTreeInfo
from pycfr.models.TreeConfig import TreeConfig


TreeParam = namedtuple(
    "TreeParam",
    [
        "player",
        "opponent",
        "player_stack",
        "opponent_stack",
        "prev_amount",
        "to_call",
        "pot",
        "max_amount",
        "min_amount",
        "spr_after_call",
        "candidates",
        "donk_candidates",
        "num_remaining_streets",
        "allin_flag",
        "num_bets",
    ],
)


@dataclass
class ActionTree:
    config: TreeConfig
    added_lines: list[list[Action]] = field(default_factory=list)
    removed_lines: list[list[Action]] = field(default_factory=list)
    root: ActionTreeNode = field(default_factory=ActionTreeNode)
    history: list[Action] = field(default_factory=list)

    def __init__(self, config: TreeConfig) -> None:
        # self.check_config(config)
        self.config = config
        self.root = ActionTreeNode(board_state=self.config.initial_state)
        # self.root.board_state = self.config.initial_state
        self.build_tree()

    def build_tree(self) -> None:
        self._build_tree_recursive(
            node=self.root, info=ActionBuildTreeInfo(stack=self.config.effective_stack)
        )

    def _build_tree_recursive(self, node: ActionTreeNode, info: ActionBuildTreeInfo) -> None:
        """_summary_.

        Args:
            node (ActionTreeNode): A mutable reference to an ActionTreeNode struct.
            info (ActionBuildTreeInfo): A BuildTreeInfo struct that contains information
            about the current state of the tree being built.

        Flow:
            If the current node is a terminal node, do nothing.
            If the current node is a chance node,
            determine the next state and player based on the current state
            and the info struct.

            Add a Chance(0) action to the current node's actions.
            Create a new child node with the determined next player and state,
            and push it to the current node's children.

            Recursively call build_tree_recursive on the new child node,
            passing in the updated info struct.

            If the current node is not a chance node,
            push the available actions to the current node's actions.

            For each action and corresponding child node,
            recursively call build_tree_recursive on the child node,
            passing in the updated info struct.

        """
        if node.is_terminal():
            pass
        elif node.is_chance():
            self.__node_is_chance(node, info)
        else:
            self.__append_actions(node, info)

    def __node_is_chance(self, node: ActionTreeNode, info: ActionBuildTreeInfo) -> None:
        print("ENT: __node_is_chance")
        if node.board_state == BoardState.Flop:
            next_state = BoardState.Turn
            if not info.allin_flag:
                next_player = PLAYER_OOP
            else:
                next_player = PLAYER_CHANCE_FLAG | PLAYER_CHANCE
        elif node.board_state == BoardState.Turn:
            next_state = BoardState.River
            next_player = PLAYER_TERMINAL_FLAG
        else:
            raise NotImplementedError

        node.actions += [Action(ActionType.Chance, value=0)]
        node.children += [
            ActionTreeNode(
                player=next_player,
                board_state=next_state,
                amount=node.amount,
                actions=[],
                children=[],
            )
        ]

        self._build_tree_recursive(
            node.children[0],
            info.create_next(player=0, action=Action(type=ActionType.Chance, value=0)),
        )

    def compute_geometric(
        self, num_streets: int, max_ratio: float, spr_after_call: float, pot: int
    ) -> int:
        ratio = ((2.0 * spr_after_call + 1.0) ** (1.0 / num_streets) - 1.0) / 2.0
        return int(round(pot * min(ratio, max_ratio)))

    def is_above_threshold(self, amount, prev_amount, pot, max_amount, config):
        new_amount_diff = amount - prev_amount
        new_pot = pot + 2 * new_amount_diff
        threshold = round(new_pot * config.force_allin_threshold)
        return max_amount <= amount + threshold

    def clamp(self, value, minimum, maximum):
        return min(maximum, max(minimum, value))

    def merge_bet_actions(
        self, actions: list[Action], pot: int, offset: int, param: float
    ) -> list[Action]:
        EPS = 1e-12

        def get_amount(action):
            if isinstance(action.type, (ActionType.Bet, ActionType.Raise, ActionType.AllIn)):
                return action.value
            else:
                return -1

        cur_amount = float("inf")
        ret = []

        for action in reversed(actions):
            amount = get_amount(action)
            if amount > 0:
                ratio = (amount - offset) / pot
                cur_ratio = (cur_amount - offset) / pot
                threshold_ratio = (cur_ratio - param) / (1.0 + param)
                if ratio < threshold_ratio * (1.0 - EPS):
                    ret.append(action)
                    cur_amount = amount
            else:
                ret.append(action)

        ret.reverse()

        return ret

    def __append_actions(self, node: ActionTreeNode, info: ActionBuildTreeInfo):
        """Pushes actions to the given ActionTreeNode bases on the provided info.

        Args:
            node (ActionTreeNode): _description_
            info (ActionBuildTreeInfo): _description_

        """
        print("ENT: __append_actions")
        param = self.__get_parameters(node, info)

        actions: list[Action] = []

        if (
            param.donk_candidates
            and info.prev_action.type == ActionType.Chance
            and info.oop_call_flag
        ):
            actions = self.__append_donk_actions(param)

        elif info.prev_action == (ActionType.Nothing or ActionType.Check or ActionType.Chance):
            actions = self.__append_bet_actions(param)
        else:
            actions = self.__response_actions(param)

        actions = self.__clamp_actions(actions, param)
        actions.sort()
        actions = list(dict.fromkeys(actions))
        actions = self.merge_bet_actions(
            actions, param.pot, param.prev_amount, self.config.merging_threshold
        )

        player_after_call = (
            PLAYER_TERMINAL_FLAG
            if node.board_state == BoardState.River
            else (PLAYER_CHANCE_FLAG | param.player)
        )

        player_after_check = param.opponent if param.player == PLAYER_OOP else player_after_call

        for action in actions:
            amount = node.amount
            if action.type == ActionType.Fold:
                next_player = PLAYER_FOLD_FLAG | param.player
            elif action.type == ActionType.Check:
                next_player = player_after_check
            elif action.type == ActionType.Call:
                amount += param.to_call
                next_player = player_after_call
            elif action.type in [ActionType.Bet, ActionType.Raise, ActionType.AllIn]:
                amount += param.to_call
                next_player = param.opponent
            else:
                raise ValueError(f"Unexpected action: {action}")

            node.actions.append(action)
            node.children.append(
                ActionTreeNode(
                    player=next_player,
                    board_state=node.board_state,
                    amount=amount,
                    # Other fields go here as needed
                )
            )

        node.actions = list(node.actions)
        node.children = list(node.children)

    def __get_parameters(self, node: ActionTreeNode, info: ActionBuildTreeInfo) -> TreeParam:
        """_summary_.

        Args:
            node (ActionTreeNode): _description_
            info (ActionBuildTreeInfo): _description_

        Returns:
            TreeParam: _description_

        Hierarchy:
            __append_actions --> __get_parameters
        """
        player: int = node.player
        player = node.player
        opponent = node.player ^ 1
        player_stack = info.stack[player]
        opponent_stack = info.stack[opponent]
        prev_amount = info.prev_amount
        to_call = player_stack - opponent_stack

        pot = self.config.starting_pot + 2 * (node.amount + to_call)
        max_amount = opponent_stack + prev_amount
        min_amount = max(prev_amount + to_call, 1)

        spr_after_call = float(opponent_stack) / float(pot)

        candidates, donk_candidates, num_remaining_streets = self.__get_candidates(
            node.board_state
        )
        allin_flag = info.allin_flag
        num_bets = info.num_bets

        return TreeParam(
            player,
            opponent,
            player_stack,
            opponent_stack,
            prev_amount,
            to_call,
            pot,
            max_amount,
            min_amount,
            spr_after_call,
            candidates,
            donk_candidates,
            num_remaining_streets,
            allin_flag,
            num_bets,
        )

    def __get_candidates(
        self, board_state: BoardState
    ) -> tuple[list[BetSizeStrategy], DonkSizeStrategy | None, int]:
        """_summary_.

        Args:
            board_state (BoardState): _description_

        Raises:
            NotImplementedError: _description_

        Returns:
            tuple[list[BetSizeStrategy], DonkSizeStrategy | None, int]: _description_

        Hierarchy:
            __append_actions --> __get_parameters --> __get_candidates
        """
        if board_state == BoardState.Flop:
            return self.config.flop_bet_sizes, None, 3
        elif board_state == BoardState.Turn:
            return self.config.turn_bet_sizes, self.config.turn_donk_sizes, 2
        elif board_state == BoardState.River:
            return self.config.river_bet_sizes, self.config.river_donk_sizes, 1
        else:
            raise NotImplementedError

    def __append_donk_actions(self, param: TreeParam) -> list[Action]:
        actions = []
        actions += [Action(ActionType.Check, value=0)]

        for donk_size in param.donk_candidates.donk_strategy:
            if donk_size.type == BetSizeType.PotRelative:
                amount = int(round(param.pot * donk_size.value))
                actions += [Action(ActionType.Bet, value=amount)]
            elif donk_size.type == BetSizeType.PrevBetRelative:
                raise NotImplementedError
            elif donk_size.type == BetSizeType.Additive:
                actions += [Action(ActionType.Bet, value=donk_size.value)]
            elif donk_size.type == BetSizeType.Geometric:
                amount = self.compute_geometric(
                    num_streets=param.num_remaining_streets,
                    max_ratio=float("inf"),
                    spr_after_call=param.spr_after_call,
                    pot=param.pot,
                )
                actions += [Action(ActionType.Bet, value=amount)]
            elif donk_size.type == BetSizeType.AllIn:
                actions += [Action(ActionType.AllIn, value=param.max_amount)]
            else:
                raise NotImplementedError

        if param.max_amount <= round(param.pot * self.config.add_allin_threshold):
            actions += [Action(ActionType.AllIn, value=param.max_amount)]

        return actions

    def __append_bet_actions(self, param: TreeParam) -> list[Action]:
        actions = []
        actions += [Action(ActionType.Check, value=0)]

        for bet_size in param.candidates:
            if bet_size.type == BetSizeType.PotRelative:
                amount = int(round(param.pot * bet_size.value))
                actions += [Action(ActionType.Bet, value=amount)]
            elif bet_size.type == BetSizeType.PrevBetRelative:
                raise NotImplementedError
            elif bet_size.type == BetSizeType.Additive:
                actions += [Action(ActionType.Bet, value=bet_size.value)]
            elif bet_size.type == BetSizeType.Geometric:
                amount = self.compute_geometric(
                    num_streets=param.num_remaining_streets,
                    max_ratio=float("inf"),
                    spr_after_call=param.spr_after_call,
                    pot=param.pot,
                )
                actions += [Action(ActionType.Bet, value=amount)]
            elif bet_size.type == BetSizeType.AllIn:
                actions += [Action(ActionType.AllIn, value=param.max_amount)]
            else:
                raise NotImplementedError

        if param.max_amount <= round(param.pot * self.config.add_allin_threshold):
            actions += [Action(ActionType.AllIn, value=param.max_amount)]

        return actions

    def __response_actions(self, param: TreeParam) -> list[Action]:
        actions = []
        actions += [Action(ActionType.Fold, value=0)]
        actions += [Action(ActionType.Call, value=0)]

        if not param.allin_flag:
            for bet_size in param.candidates:
                if bet_size.type == BetSizeType.PotRelative:
                    amount = param.prev_amount + int(round(param.pot * bet_size.value))
                    actions += [Action(ActionType.Raise, value=amount)]
                elif bet_size.type == BetSizeType.PrevBetRelative:
                    amount = int(round(param.prev_amount * bet_size.value))
                    actions += [Action(ActionType.Raise, value=amount)]
                elif bet_size.type == BetSizeType.Additive:
                    # to do: raise capも反映する必要がある.
                    actions += [
                        Action(ActionType.Raise, value=(param.prev_amount + bet_size.value))
                    ]
                elif bet_size.type == BetSizeType.Geometric:
                    num_streets = (
                        max(param.num_remaining_streets - param.num_bets + 1, 1)
                        if bet_size.value[0] == 0
                        else max(bet_size.value[0] - param.num_bets + 1, 1)
                    )
                    amount = self.compute_geometric(
                        num_streets=num_streets,
                        max_ratio=float("inf"),
                        spr_after_call=param.spr_after_call,
                        pot=param.pot,
                    )
                    actions += [Action(ActionType.Raise, value=(amount + param.prev_amount))]
                elif bet_size.type == BetSizeType.AllIn:
                    actions += [Action(ActionType.AllIn, value=param.max_amount)]

                else:
                    raise NotImplementedError

        if param.max_amount <= round(param.pot * self.config.add_allin_threshold):
            actions += [Action(ActionType.AllIn, value=param.max_amount)]
        return actions

    def __clamp_actions(self, actions: list[Action], param: TreeParam) -> list[Action]:
        for action in actions:
            if action.type == ActionType.Bet:
                clamped = self.clamp(action.value, param.min_amount, param.max_amount)
                if self.is_above_threshold(
                    clamped, param.prev_amount, param.pot, param.max_amount, self.config
                ):
                    action = Action(ActionType.AllIn, value=param.max_amount)
                elif clamped != action.value:
                    action = Action(ActionType.Bet, value=clamped)
                else:
                    pass
            elif action.type == ActionType.Raise:
                clamped = self.clamp(action.value, param.min_amount, param.max_amount)
                if self.is_above_threshold(
                    clamped, param.prev_amount, param.pot, param.max_amount, self.config
                ):
                    action = Action(ActionType.AllIn, value=param.max_amount)
                elif clamped != action.value:
                    action = Action(ActionType.Raise, value=clamped)
                else:
                    pass
            else:
                pass
        return actions

    def add_action(self, action: Action) -> None:
        action_line = self.history.copy()
        action_line.append(action)
        self.add_line(action_line)

    def add_line(self, line: list[Action]) -> None:
        """_summary_.

        Args:
            line (list[Action]): _description_

        Hierarchy:
            add_action --> add_line --> _add_line_recursive
        """
        removed_index = next((i for i, x in enumerate(self.removed_lines) if x == line), None)
        is_replaced = self._add_line_recursive(
            node=self.root,
            line=line,
            was_removed=removed_index is not None,
            info=ActionBuildTreeInfo(stack=self.config.effective_stack),
        )
        if removed_index is not None:
            self.removed_lines.pop(removed_index)
        else:
            line_copy = line.copy()
            if is_replaced:
                last_action = line_copy[-1]

            self.added_lines

    def _add_line_recursive(
        self,
        node: ActionTreeNode,
        line: list[Action],
        was_removed: bool,
        info: ActionBuildTreeInfo,
    ):
        """Recursive function to add a given line to the tree.

        Args:
            node (ActionTreeNode): _description_
            line (list[Action]): _description_
            was_removed (bool): _description_
            info (ActionBuildTreeInfo): _description_

        Hierarchy:
            add_line --> _add_line_recursive
        """
        if not line:
            raise ValueError
        if node.is_terminal():
            raise ValueError
        if node.is_chance():
            return self._add_line_recursive(node.children[0], line, was_removed, info.cre)

    def invalid_terminals(self) -> list[list[Action]]:
        """Returns a list of all terminal nodes that should not be.

        Returns:
            list[list[Action]]: _description_

        Hierarchy:
            Game.update_config --> invalid_terminals
        """
        ret: list[list[Action]] = []
        line: list[Action] = []
        self._invalid_terminals_recursive(self.root, ret, line)
        return ret

    def _invalid_terminals_recursive(
        self, node: ActionTreeNode, result: list[list[Action]], line: list[Action]
    ) -> None:
        """Recursive function to enumerate all invalid terminal nodes.

        Hierarchy:
            invalid_terminals --> invalid_terminals_recursive
            invalid_terminals_recursive --> invalid_terminals_recursive
        """
        if node.is_terminal():
            pass
        elif not node.children:
            result.append(line.copy())
        elif node.is_chance():
            self._invalid_terminals_recursive(node.children[0], result, line)
        else:
            for action, child in zip(node.actions, node.children):
                line.append(action)
                self._invalid_terminals_recursive(child, result, line)
                line.pop()

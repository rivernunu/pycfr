import pytest

from pycfr.models.Action import Action, ActionType
from pycfr.models.BuildTreeInfo import ActionBuildTreeInfo


class TestNormalSample:
    def test_create_instance_with_default_arguments(self) -> None:
        action_build_tree_info = ActionBuildTreeInfo()
        assert action_build_tree_info.prev_action == Action(ActionType.Nothing, value=None)
        assert action_build_tree_info.num_bets == 0
        assert action_build_tree_info.allin_flag is False
        assert action_build_tree_info.oop_call_flag is False
        assert action_build_tree_info.stack == [0, 0]
        assert action_build_tree_info.prev_amount == 0

    def test_create_instance_with_custom_arguments(self) -> None:
        prev_action = Action(ActionType.Bet, value=10)
        num_bets = 2
        allin_flag = True
        oop_call_flag = False
        stack = [100, 200]
        prev_amount = 20

        action_build_tree_info = ActionBuildTreeInfo(
            prev_action=prev_action,
            num_bets=num_bets,
            allin_flag=allin_flag,
            oop_call_flag=oop_call_flag,
            stack=stack,
            prev_amount=prev_amount,
        )

        assert action_build_tree_info.prev_action == prev_action
        assert action_build_tree_info.num_bets == num_bets
        assert action_build_tree_info.allin_flag == allin_flag
        assert action_build_tree_info.oop_call_flag == oop_call_flag
        assert action_build_tree_info.stack == stack
        assert action_build_tree_info.prev_amount == prev_amount

    # Test that the create_next method of ActionBuildTreeInfo class correctly handles ActionType.Raise with value=None.
    def test_create_next_with_raise_and_none_value(self):
        prev_action = Action(ActionType.Nothing, value=None)
        num_bets = 0
        allin_flag = False
        oop_call_flag = False
        stack = [100, 100]
        prev_amount = 0

        action_build_tree_info = ActionBuildTreeInfo(
            prev_action=prev_action,
            num_bets=num_bets,
            allin_flag=allin_flag,
            oop_call_flag=oop_call_flag,
            stack=stack,
            prev_amount=prev_amount,
        )

        player = 0
        action = Action(ActionType.Raise, value=None)

        next_action_build_tree_info = action_build_tree_info.create_next(player, action)

        assert next_action_build_tree_info.prev_action == action
        assert next_action_build_tree_info.num_bets == num_bets + 1
        assert next_action_build_tree_info.allin_flag == False
        assert next_action_build_tree_info.oop_call_flag == oop_call_flag
        assert next_action_build_tree_info.stack == [100, 100]
        assert next_action_build_tree_info.prev_amount == prev_amount

    # Test that the create_next method of the ActionBuildTreeInfo class correctly handles the ActionType.AllIn action with a value of 0.
    def test_create_next_allin_value_zero(self):
        prev_action = Action(ActionType.Nothing, value=None)
        num_bets = 0
        allin_flag = False
        oop_call_flag = False
        stack = [100, 100]
        prev_amount = 0

        action_build_tree_info = ActionBuildTreeInfo(
            prev_action,
            num_bets,
            allin_flag,
            oop_call_flag,
            stack,
            prev_amount,
        )

        player = 0
        action = Action(ActionType.AllIn, value=0)

        next_action_build_tree_info = action_build_tree_info.create_next(player, action)

        assert next_action_build_tree_info.prev_action == action
        assert next_action_build_tree_info.num_bets == num_bets + 1
        assert next_action_build_tree_info.allin_flag == True
        assert next_action_build_tree_info.oop_call_flag == oop_call_flag
        assert next_action_build_tree_info.stack == [100, 100]
        assert next_action_build_tree_info.prev_amount == prev_amount

    # Test that the create_next method of ActionBuildTreeInfo class behaves correctly when called with ActionType.Raise and action.value=0.
    def test_create_next_with_raise_and_zero_value(self):
        prev_action = Action(ActionType.Nothing, value=None)
        num_bets = 0
        allin_flag = False
        oop_call_flag = False
        stack = [100, 100]
        prev_amount = 0

        action_build_tree_info = ActionBuildTreeInfo(
            prev_action,
            num_bets,
            allin_flag,
            oop_call_flag,
            stack,
            prev_amount,
        )

        player = 0
        action = Action(ActionType.Raise, value=0)

        result = action_build_tree_info.create_next(player, action)

        assert result.prev_action == action
        assert result.num_bets == 1
        assert result.allin_flag == False
        assert result.oop_call_flag == False
        assert result.stack == [100, 100]
        assert result.prev_amount == 0

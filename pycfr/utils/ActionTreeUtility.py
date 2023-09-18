"""util.

aaa.
"""

from pycfr.models.Action import Action, ActionType


class ActionTreeUtility:
    @staticmethod
    def compute_geometric(
        num_streets: int, max_ratio: float, spr_after_call: float, pot: int
    ) -> int:
        """Calculates geometric bet size.

        Args:
            num_streets (int): The number of streets in the game.
            max_ratio (float): The maximum ratio allowed.
            spr_after_call (float): The SPR (Stack-to-Pot Ratio) after a call.
            pot (int): The size of the pot.

        Returns:
            int: The calculated geometric value.

        Example:
            >>> ActionTreeUtility.compute_geometric(3, float('inf'), 17, 6)
            7
            >>> ActionTreeUtility.compute_geometric(2, float('inf'), 5, 20)
            23
            >>> ActionTreeUtility.compute_geometric(1, float('inf'), 1, 66)
            66
        """
        ratio = ((2.0 * spr_after_call + 1.0) ** (1.0 / num_streets) - 1.0) / 2.0
        return int(round(pot * min(ratio, max_ratio)))

    @staticmethod
    def is_above_threshold(
        amount: int, prev_amount: int, pot: int, max_amount: int, force_allin_threshold: float
    ) -> bool:
        new_amount_diff = amount - prev_amount
        new_pot = pot + 2 * new_amount_diff
        threshold = round(new_pot * force_allin_threshold)
        return max_amount <= amount + threshold

    @staticmethod
    def clamp(value, minimum, maximum):
        return min(maximum, max(minimum, value))

    @staticmethod
    def merge_bet_actions(
        actions: list[Action], pot: int, offset: int, param: float
    ) -> list[Action]:
        EPS = 1e-12

        def get_amount(action):
            if action.type == (ActionType.Bet or ActionType.Raise or ActionType.AllIn):
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

from pycfr.models.Suitedness import Suitedness, SuitednessType
from pycfr.utils.CardParser import CardParser


class RangeIndex:
    @staticmethod
    def extract(rank1: int, rank2: int, suitedness: Suitedness) -> list[int]:
        """Returns a list of indices based on the given ranks and suitedness.

        Args:
            rank1 (int): The rank of the first card.
            rank2 (int): The rank of the second card.
            suitedness (Suitedness): An instance of the `Suitedness` class representing the desired suitedness of the cards.

        Returns:
            list[int]: A list of indices representing the possible combinations of cards based on the given ranks and suitedness.

        Raises:
            ValueError: If the given parameters do not meet any of the specified conditions.

        Example:
            >>> RangeIndex.extract(0, 0, Suitedness(SuitednessType.Specific, (0,1))
            [0]
            >>> RangeIndex.extract(0, 0, Suitedness(SuitednessType.All))
            [0, 1, 2, 51, 52, 101]
        """
        if rank1 == rank2:
            if suitedness.type == SuitednessType.All:
                return RangeIndex._pair_indices(rank1)
            elif suitedness.type == SuitednessType.Specific:
                if suitedness.suit is not None:
                    return [
                        CardParser.card_pair_to_index(
                            4 * rank1 + suitedness.suit[0], 4 * rank1 + suitedness.suit[1]
                        )
                    ]
                else:
                    raise ValueError
            else:
                raise ValueError(f"invalid suitedness with a pair. {suitedness}")
        else:
            if suitedness.type == SuitednessType.Suited:
                return RangeIndex._suited_indices(rank1, rank2)
            elif suitedness.type == SuitednessType.Offsuit:
                return RangeIndex._offsuit_indices(rank1, rank2)
            elif suitedness.type == SuitednessType.All:
                return RangeIndex._not_pair_indices(rank1, rank2)
            elif suitedness.type == SuitednessType.Specific:
                if suitedness.suit is not None:
                    return [
                        CardParser.card_pair_to_index(
                            4 * rank1 + suitedness.suit[0], 4 * rank1 + suitedness.suit[1]
                        )
                    ]
                else:
                    raise ValueError
            else:
                raise ValueError(f"suitedness was not defined. {suitedness}")

    @staticmethod
    def _pair_indices(rank: int) -> list[int]:
        result: list[int] = []

        for i in range(4):
            for j in range(i + 1, 4):
                result.append(CardParser.card_pair_to_index(4 * rank + i, 4 * rank + j))

        return result

    @staticmethod
    def _not_pair_indices(rank1: int, rank2: int) -> list[int]:
        result: list[int] = []

        for i in range(4):
            for j in range(4):
                result.append(CardParser.card_pair_to_index(4 * rank1 + i, 4 * rank2 + j))

        return result

    @staticmethod
    def _suited_indices(rank1: int, rank2: int) -> list[int]:
        result: list[int] = []

        for i in range(4):
            result.append(CardParser.card_pair_to_index(4 * rank1 + i, 4 * rank2 + i))

        return result

    @staticmethod
    def _offsuit_indices(rank1: int, rank2: int) -> list[int]:
        """Returns a list of indices representing the offsuit combinations of two card ranks.

        Args:
            rank1 (int): The rank of the first card. Should be an integer between 0 and 12.
            rank2 (int): The rank of the second card. Should be an integer between 0 and 12.

        Returns:
            list[int]: A list of indices representing the offsuit combinations of the two ranks.

        Example:
            >>> RangeIndex.extract(12, 11, Suitedness(SuitednessType.Offsuit))
            [1307, 1312, 1316, 1302, 1313, 1317, 1303, 1309, 1318, 1304, 1310, 1315]
        """
        result: list[int] = []
        for i in range(4):
            for j in range(4):
                if i != j:
                    result.append(CardParser.card_pair_to_index(4 * rank1 + i, 4 * rank2 + j))

        return result

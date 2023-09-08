from pycfr.models.Suitedness import Suitedness
from pycfr.utils.CardParser import CardParser


class CardIndex:
    @staticmethod
    def indices_with_suitedness(rank1: int, rank2: int, suitedness: Suitedness) -> list[int]:
        if rank1 == rank2:
            if suitedness.All:
                return CardIndex._pair_indices(rank1)
            elif suitedness.Specific:
                return [
                    CardParser.card_pair_to_index(
                        4 * rank1 + suitedness.Specific[0], 4 * rank1 + suitedness.Specific[1]
                    )
                ]
            else:
                raise ValueError
        else:
            if suitedness.Suited:
                return CardIndex._suited_indices(rank1, rank2)
            elif suitedness.Offsuit:
                return CardIndex._offsuit_indices(rank1, rank2)
            elif suitedness.All:
                return CardIndex._nonpair_indices(rank1, rank2)
            elif suitedness.Specific:
                return [
                    CardParser.card_pair_to_index(
                        4 * rank1 + suitedness.Specific[0], 4 * rank1 + suitedness.Specific[1]
                    )
                ]
            else:
                raise ValueError

    @staticmethod
    def _pair_indices(rank: int) -> list[int]:
        result: list[int] = []

        for i in range(4):
            for j in range(i + 1, 4):
                result.append(CardParser.card_pair_to_index(4 * rank + i, 4 * rank + j))

        return result

    @staticmethod
    def _nonpair_indices(rank1: int, rank2: int) -> list[int]:
        result: list[int] = []

        for i in range(4):
            for j in range(4):
                result.append(CardParser.card_pair_to_index(4 * rank1 + i, 4 * rank2 + j))

        return result

    @staticmethod
    def _suited_indices(rank1: int, rank2: int) -> list[int]:
        result: list[int] = []

        for i in range(4):
            result.append(CardParser.card_pair_to_index(4 * rank1 + i, 4 * rank2 * i))

        return result

    @staticmethod
    def _offsuit_indices(rank1: int, rank2: int) -> list[int]:
        result: list[int] = []
        for i in range(4):
            for j in range(4):
                if i != j:
                    result.append(CardParser.card_pair_to_index(4 * rank1 + i, 4 * rank2 + j))

        return result

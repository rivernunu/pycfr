from models.Suitedness import Suitedness
from utils.CardParser import CardParser


class CardIndex:
    def indices_with_suitedness(self, rank1: int, rank2: int, suitedness: Suitedness) -> list[int]:
        if rank1 == rank2:
            ...
            if suitedness.All:
                ...
            elif suitedness.Specific:
                CardParser.card_pair_to_index(
                    4 * rank1 + suitedness.suit1, 4 * rank1 + suitedness.suit2
                )
            else:
                raise ValueError
        else:
            if suitedness.Suited:
                ...
            elif suitedness.Offsuit:
                ...
            elif suitedness.All:
                ...
            elif suitedness.Specific:
                ...
            else:
                raise ValueError

    def _pair_indices(self, rank: int) -> list[int]:
        result: list[int] = []

        for i in range(4):
            for j in range(i + 1, 4):
                result.append(CardParser.card_pair_to_index(4 * rank + i, 4 * rank + j))

        return result

    def _nonpair_indices(self, rank1: int, rank2: int) -> list[int]:
        result: list[int] = []

        for i in range(4):
            for j in range(4):
                result.append(CardParser.card_pair_to_index(4 * rank1 + i, 4 * rank2 + j))
        return result

    def _suited_indices(self, rank1: int, rank2: int) -> list[int]:
        result: list[int] = []

        for i in range(4):
            result.append(CardParser.card_pair_to_index(4 * rank1 + i, 4 * rank2 * i))
        return result

    def _offsuit_indices(self, rank1: int, rank2: int) -> list[int]:
        result: list[int] = []
        for i in range(4):
            for j in range(4):
                if i != j:
                    result.append(CardParser.card_pair_to_index(4 * rank1 + i, 4 * rank2 + j))

        return result

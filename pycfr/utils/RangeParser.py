from collections.abc import Iterator

from pycfr.models.Suitedness import Suitedness
from pycfr.utils.CardParser import CardParser
from pycfr.utils.RangeIndex import RangeIndex


class RangeParser:
    @staticmethod
    def from_sanitized_str(range_string_representation: str) -> list[float]:
        """Converts a string representation of a range into a list of floats.

        Args:
            range_string_representation (str): A string representation of a range,
                where each range is separated by a comma.

        Returns:
            list[float]: A list of floats representing the weights
                of each possible combination of cards in the range.
        """
        data: list[float] = [0.0] * 1326
        range_list: list[str] = range_string_representation.split(",")

        for range_str in reversed(range_list):
            range_part, weight = range_str.split(":")
            weight = float(weight) if weight else 1.0

            if "-" in range_part:
                RangeParser._update_with_dash_range(range_part, weight, data)
            elif "+" in range_part:
                RangeParser._update_with_plus_range(range_part, weight, data)
            else:
                RangeParser._update_with_singleton(range_part, weight, data)

        return data

    @staticmethod
    def _update_with_dash_range(range_: str, weight: float, data: list[float]) -> None:
        combo_pair: list[str] = range_.split("-")
        rank11, rank12, suitedness = RangeParser._parse_singleton(combo_pair[0])
        rank21, rank22, suitedness2 = RangeParser._parse_singleton(combo_pair[1])
        gap: int = rank11 - rank12
        gap2: int = rank21 - rank22
        if suitedness != suitedness2:
            raise ValueError
        elif gap == gap2:
            if rank11 > rank21:
                for i in range(rank21, rank11 + 1):
                    RangeParser.set_weight(
                        RangeIndex.extract(i, i - gap, suitedness), weight, data
                    )
            else:
                raise ValueError
        elif rank11 == rank21:
            if rank12 > rank22:
                for i in range(rank22, rank12 + 1):
                    RangeParser.set_weight(RangeIndex.extract(rank11, i, suitedness), weight, data)
            else:
                raise ValueError
        else:
            raise ValueError

    @staticmethod
    def _update_with_plus_range(range_: str, weight: float, data: list[float]) -> None:
        lowest_combo: str = range_[:-1]
        rank1, rank2, suitedness = RangeParser._parse_singleton(lowest_combo)
        gap = rank1 - rank2
        if gap <= 1:
            for i in range(rank1, 13):
                RangeParser.set_weight(RangeIndex.extract(i, i - gap, suitedness), weight, data)
        else:
            for i in range(rank2, rank1):
                RangeParser.set_weight(RangeIndex.extract(rank1, i, suitedness), weight, data)

    @staticmethod
    def _update_with_singleton(combo: str, weight: float, data: list[float]) -> None:
        rank1, rank2, suitedness = RangeParser._parse_singleton(combo)
        indices = RangeIndex.extract(rank1, rank2, suitedness)
        RangeParser.set_weight(indices, weight, data)

    def from_str(self, ranges: str) -> list[float]:
        ...

    @staticmethod
    def set_weight(indices: list[int], weight: float, data: list[float]) -> None:
        """Update the weights of specific indices in a given data list.

        Args:
            indices: A list of integers representing the indices to be updated in the data list.
            weight: A float value representing the weight to be assigned to the specified indices.
            data: A list of floats representing the data to be updated.

        Returns:
            None. The data list is modified in-place.
        """
        for index in indices:
            if index < len(data):
                data[index] = weight

    @staticmethod
    def _parse_singleton(combo: str) -> tuple[int, int, Suitedness]:
        if len(combo) == 4:
            return RangeParser.__parse_simple_singleton(combo)
        else:
            return RangeParser.__parse_compound_singleton(combo)

    @staticmethod
    def __parse_simple_singleton(combo: str) -> tuple[int, int, Suitedness]:
        chars: Iterator[str] = iter(combo)
        rank1: int = CardParser.char_to_rank(next(chars))
        suit1: int = CardParser.char_to_suit(next(chars))
        rank2: int = CardParser.char_to_rank(next(chars))
        suit2: int = CardParser.char_to_suit(next(chars))

        if rank1 < rank2:
            raise SyntaxError

        if rank1 == rank2 and suit1 == suit2:
            raise SyntaxError

        return rank1, rank2, Suitedness(Specific=(suit1, suit2))

    @staticmethod
    def __parse_compound_singleton(combo: str) -> tuple[int, int, Suitedness]:
        chars: Iterator[str] = iter(combo)
        rank1: int = CardParser.char_to_rank(next(chars))
        rank2: int = CardParser.char_to_rank(next(chars))

        try:
            suit = next(chars)
            if suit == "o":
                suitedness = Suitedness(Offsuit=True)
            elif suit == "s":
                suitedness = Suitedness(Suited=True)
            else:
                ValueError
        except StopIteration:
            suitedness = Suitedness(All=True)

        if rank1 < rank2:
            raise SyntaxError

        if rank1 == rank2 & suitedness.All:
            raise SyntaxError

        return rank1, rank2, suitedness

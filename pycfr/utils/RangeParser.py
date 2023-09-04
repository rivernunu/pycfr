from typing import Iterator

from models.Suitedness import Suitedness
from utils.CardIndex import CardIndex
from utils.CardParser import CardParser


class RangeParser:
    def from_sanitized_str(self, ranges: str) -> list[float]:
        data: list[float] = [0.0] * 1326
        range_list: list[str] = ranges.split(",")

        for range_str in reversed(range_list):
            split = range_str.split(":")
            range_part = split[0]
            weight = float(split[1]) if len(split) > 1 else 1.0

            if "-" in range_part:
                self.update_with_dash_range(range_part, weight, data)
            elif "+" in range_part:
                self.update_with_plus_range(range_part, weight, data)
            else:
                self.update_with_singleton(range_part, weight, data)

        return data

    def update_with_dash_range(self, range_: str, weight: float, data: list[float]) -> None:
        combo_pair: list[str] = range_.split("-")
        rank11, rank12, suitedness = self._parse_singleton(combo_pair[0])
        rank21, rank22, suitedness2 = self._parse_singleton(combo_pair[1])
        gap: int = rank11 - rank12
        gap2: int = rank21 - rank22
        if suitedness != suitedness2:
            raise ValueError
        elif gap == gap2:
            if rank11 > rank21:
                for i in range(rank21, rank11 + 1):
                    self.set_weight(
                        CardIndex.indices_with_suitedness(i, i - gap, suitedness), weight, data
                    )
            else:
                raise ValueError
        elif rank11 == rank21:
            if rank12 > rank22:
                for i in range(rank22, rank12 + 1):
                    self.set_weight(
                        CardIndex.indices_with_suitedness(rank11, i, suitedness), weight, data
                    )
            else:
                raise ValueError
        else:
            raise ValueError

    def update_with_plus_range(self, range_: str, weight: float, data: list[float]) -> None:
        lowest_combo: str = range_[:-1]
        rank1, rank2, suitedness = self._parse_singleton(lowest_combo)
        gap = rank1 - rank2
        if gap <= 1:
            for i in range(rank1, 13):
                self.set_weight(
                    CardIndex.indices_with_suitedness(i, i - gap, suitedness), weight, data
                )
        else:
            for i in range(rank2, rank1):
                self.set_weight(
                    CardIndex.indices_with_suitedness(rank1, i, suitedness), weight, data
                )

    def update_with_singleton(self, combo: str, weight: float, data: list[float]) -> None:
        rank1, rank2, suitedness = self._parse_singleton(combo)
        indices = CardIndex.indices_with_suitedness(rank1, rank2, suitedness)
        self.set_weight(indices, weight, data)

    def from_str(self, ranges: str) -> list[float]:
        ...

    def set_weight(self, indices: list[int], weight: float, data: list[float]) -> None:
        for index in indices:
            data[index] = weight

    def _parse_singleton(self, combo: str) -> tuple[int, int, Suitedness]:
        if len(combo) == 4:
            return self.__parse_simple_singleton(combo)
        else:
            return self.__parse_compound_singleton(combo)

    def __parse_simple_singleton(self, combo: str) -> tuple[int, int, Suitedness]:
        chars: Iterator[str] = iter(combo)
        rank1: int = CardParser.char_to_rank(chars)
        suit1: int = CardParser.char_to_suit(chars)
        rank2: int = CardParser.char_to_rank(chars)
        suit2: int = CardParser.char_to_suit(chars)

        if rank1 < rank2:
            raise SyntaxError

        if rank1 == rank2 and suit1 == suit2:
            raise SyntaxError

        return rank1, rank2, Suitedness(Specific=True, suit1=suit1, suit2=suit2)

    def __parse_compound_singleton(self, combo: str) -> tuple[int, int, Suitedness]:
        chars: Iterator[str] = iter(combo)
        rank1: int = CardParser.char_to_rank(chars)
        rank2: int = CardParser.char_to_rank(chars)

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

        if rank1 == rank2 & suitedness.all:
            raise SyntaxError

        return rank1, rank2, Suitedness

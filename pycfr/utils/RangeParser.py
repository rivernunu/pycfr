from typing import Iterator
from utils.CardIndex import CardIndex
from models.Suitedness import Suitedness
from utils.CardParser import CardParser


class RangeParser:
    def from_sanitized_str(self, ranges: str) -> list[float]:
        ...

    def from_str(self, ranges: str) -> list[float]:
        ...

    def _parse_singleton(self, combo: str) -> list[int | Suitedness]:
        if len(combo) == 4:
            return self._parse_simple_singleton(combo)
        else:
            return self._parse_compound_singleton(combo)

    def _parse_simple_singleton(self, combo: str) -> list[int | Suitedness]:
        chars: Iterator[str] = iter(combo)
        rank1: int = CardParser.char_to_rank(chars)
        suit1: int = CardParser.char_to_suit(chars)
        rank2: int = CardParser.char_to_rank(chars)
        suit2: int = CardParser.char_to_suit(chars)

        if rank1 < rank2:
            raise SyntaxError

        if rank1 == rank2 and suit1 == suit2:
            raise SyntaxError

        return [rank1, rank2, Suitedness(Specific=[suit1, suit2])]

    def _parse_compound_singleton(self, combo: str) -> list[int | Suitedness]:
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

        return [rank1, rank2, Suitedness]

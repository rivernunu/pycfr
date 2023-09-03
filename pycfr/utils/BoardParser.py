from typing import Iterator

from utils.CardParser import CardParser


class BoardParser:
    def parse_board_str(self, string: str) -> list[int] | int:
        if len(string) == 2:
            return self._card_from_str(string)
        elif len(string) == 6:
            return self._flop_from_str(string)
        else:
            raise ValueError

    def _flop_from_str(self, string: str) -> list[int]:
        result = [0] * 3
        chars = iter(string)

        result[0] = self._card_from_chars(chars)
        result[1] = self._card_from_chars(chars)
        result[2] = self._card_from_chars(chars)

        result.sort()

        return result

    def _card_from_str(self, string: str) -> int:
        chars = iter(string)
        result = self._card_from_chars(chars)

        return result

    def _card_from_chars(self, chars: Iterator[str]) -> int:
        rank_char = next(chars)
        suit_char = next(chars)

        rank = CardParser.char_to_rank(rank_char)
        suit = CardParser.char_to_suit(suit_char)

        return (rank << 2) | suit

from typing import Iterator


class CardParser:
    def parse_board_str(self, string: str) -> list[int] | int:
        if len(string) == 2:
            return self.card_from_str(string)
        elif len(string) == 6:
            return self.flop_from_str(string)
        else:
            raise ValueError

    def flop_from_str(self, string: str) -> list[int]:
        result = [0] * 3
        chars = iter(string)

        result[0] = self.card_from_chars(chars)
        result[1] = self.card_from_chars(chars)
        result[2] = self.card_from_chars(chars)

        result.sort()

        return result

    def card_from_str(self, string: str) -> int:
        chars = iter(string)
        result = self.card_from_chars(chars)

        return result

    def card_from_chars(self, chars: Iterator[str]) -> int:
        rank_char = next(chars)
        suit_char = next(chars)

        rank = self.char_to_rank(rank_char)
        suit = self.char_to_suit(suit_char)

        return (rank << 2) | suit

    def char_to_rank(self, rank_str: str) -> int:
        rank_map: dict[str, int] = {
            "A": 12,
            "K": 11,
            "Q": 10,
            "J": 9,
            "T": 8,
            "9": 7,
            "8": 6,
            "7": 5,
            "6": 4,
            "5": 3,
            "4": 2,
            "3": 1,
            "2": 0,
        }
        rank_str = rank_str.upper()
        if rank_str in rank_map:
            return rank_map[rank_str]
        else:
            raise ValueError(f"Expected rank character: {rank_str}")

    def char_to_suit(self, suit_str: str) -> int:
        suit_map = {"c": 0, "d": 1, "h": 2, "s": 3}

        if suit_str in suit_map:
            return suit_map[suit_str]
        else:
            raise ValueError(f"Expected suit character: {suit_str}")

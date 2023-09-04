import pytest

from pycfr.utils.CardParser import CardParser


class TestNormalSuite:
    @pytest.mark.parametrize(
        "rank_str, expected",
        [
            ("A", 12),
            ("K", 11),
            ("Q", 10),
            ("J", 9),
            ("T", 8),
            ("9", 7),
            ("8", 6),
            ("7", 5),
            ("6", 4),
            ("5", 3),
            ("4", 2),
            ("3", 1),
            ("2", 0),
        ],
    )
    def test_char_to_rank(self, rank_str: str, expected: int) -> None:
        assert CardParser.char_to_rank(rank_str) == expected

    @pytest.mark.parametrize("suit_str, expected", [("c", 0), ("d", 1), ("h", 2), ("s", 3)])
    def test_char_to_suit(self, suit_str: str, expected: int) -> None:
        assert CardParser.char_to_suit(suit_str) == expected

    @pytest.mark.parametrize("card1, card2, expect", [(1, 2, 0), (2, 3, 1), (50, 51, 1325)])
    def test_card_pair_to_index(self, card1: int, card2: int, expect: int) -> None:
        assert CardParser.card_pair_to_index(card1, card2) == expect

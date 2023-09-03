import pytest

from pycfr.utils.BoardParser import CardParser


@pytest.fixture
def card_parser():
    return CardParser()


def test_parse_board_str_valid_length(card_parser):
    string = "AdKs"
    with pytest.raises(ValueError):
        card_parser.parse_board_str(string)


def test_parse_board_str_invalid_length(card_parser):
    string = "AhKdJsQc"
    with pytest.raises(ValueError):
        card_parser.parse_board_str(string)


def test_flop_from_str(card_parser):
    string = "2c3d4h"
    result = card_parser.flop_from_str(string)
    assert isinstance(result, list)
    assert len(result) == 3
    assert result == [0, 5, 10]


def test_card_from_str(card_parser):
    string = "Ad"
    result = card_parser.card_from_str(string)
    assert isinstance(result, int)


def test_char_to_rank(card_parser):
    rank_str = "A"
    result = card_parser.char_to_rank(rank_str)
    assert isinstance(result, int)
    assert result == 12


def test_char_to_suit(card_parser):
    suit_str = "c"
    result = card_parser.char_to_suit(suit_str)
    assert isinstance(result, int)
    assert result == 0


def test_card_pair_to_index(card_parser):
    ...

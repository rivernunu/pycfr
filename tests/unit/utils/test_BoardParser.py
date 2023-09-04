"""Pytest::Unit test of BoardParser.

Test Suites:
    - TestNormalSuite: Test suite for normal execution scenarios.
    - TestExceptionSuite: Test suite for exceptional scenarios.

Fixtures:
    - board_parser: Fixture that returns an instance of BoardParser for testing.
"""
import pytest

from pycfr.utils.BoardParser import BoardParser


@pytest.fixture
def board_parser() -> BoardParser:
    """Fixture that returns an instance of BoardParser for testing.

    Returns:
        BoardParser: An instance of the BoardParser class.
    """
    return BoardParser()


class TestNormalSuite:
    """Test suite for normal execution scenarios.

    Test Methods:
        - test_flop: Test case to check if the board string is parsed correctly.
        - test_turn_or_river: Test case to check if the board string is parsed correctly.
    """

    @pytest.mark.parametrize(
        "string, expected", [("2c3d4h", [0, 5, 10]), ("AsAhKs", [47, 50, 51])]
    )
    def test_flop(self, board_parser: BoardParser, string: str, expected: list[int]) -> None:
        """Test case to check if the board string is parsed correctly.

        Args:
            board_parser (BoardParser): The BoardParser instance.
            string (str): The input board string.
            expected (list[int]): The expected parsed result.

        Returns:
            None
        """
        assert board_parser.parse_board_str(string) == expected

    @pytest.mark.parametrize("string, expected", [("2c", 0), ("As", 51)])
    def test_turn_or_river(self, board_parser: BoardParser, string: str, expected: int) -> None:
        """Test case to check if the board string is parsed correctly.

        Args:
            board_parser (BoardParser): The BoardParser instance.
            string (str): The input board string.
            expected (int): The expected parsed result.

        Returns:
            None
        """
        assert board_parser.parse_board_str(string) == expected


class TestExceptionSuite:
    """Test suite for exceptional scenarios.

    Test Methods:
        - test_parse_board_str_invalid_type: ...
        - test_parse_board_str_invalid_length: ...
    """

    @pytest.mark.parametrize("string", [{}, 1])
    def test_parse_board_str_invalid_type(self, board_parser: BoardParser, string: str) -> None:
        """Test case to check if a TypeError is raised when a board string is not str type.

        Args:
            board_parser (BoardParser): The BoardParser instance.
            string (str): The input board string.

        Returns:
            None
        """
        with pytest.raises(TypeError):
            board_parser.parse_board_str(string)

    @pytest.mark.parametrize("string", ["", "A", "AdAc", "AhKdJsQc", "AsKsQsJsTs"])
    def test_parse_board_str_invalid_length(self, board_parser: BoardParser, string: str) -> None:
        """Test case to check if a ValueError is raised when a board string has an invalid length.

        Args:
            board_parser (BoardParser): The BoardParser instance.
            string (str): The input board string.

        Returns:
            None
        """
        with pytest.raises(ValueError):
            board_parser.parse_board_str(string)

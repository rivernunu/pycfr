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
        """
        assert board_parser.parse(string) == expected

    @pytest.mark.parametrize(
        "string, expected",
        [
            ("2c", [0]),
            ("2d", [1]),
            ("2h", [2]),
            ("2s", [3]),
            ("3c", [4]),
            ("3d", [5]),
            ("3h", [6]),
            ("3s", [7]),
            ("4c", [8]),
            ("4d", [9]),
            ("4h", [10]),
            ("4s", [11]),
            ("5c", [12]),
            ("5d", [13]),
            ("5h", [14]),
            ("5s", [15]),
            ("6c", [16]),
            ("6d", [17]),
            ("6h", [18]),
            ("6s", [19]),
            ("7c", [20]),
            ("7d", [21]),
            ("7h", [22]),
            ("7s", [23]),
            ("8c", [24]),
            ("8d", [25]),
            ("8h", [26]),
            ("8s", [27]),
            ("9c", [28]),
            ("9d", [29]),
            ("9h", [30]),
            ("9s", [31]),
            ("Tc", [32]),
            ("Td", [33]),
            ("Th", [34]),
            ("Ts", [35]),
            ("Jc", [36]),
            ("Jd", [37]),
            ("Jh", [38]),
            ("Js", [39]),
            ("Qc", [40]),
            ("Qd", [41]),
            ("Qh", [42]),
            ("Qs", [43]),
            ("Kc", [44]),
            ("Kd", [45]),
            ("Kh", [46]),
            ("Ks", [47]),
            ("Ac", [48]),
            ("Ad", [49]),
            ("Ah", [50]),
            ("As", [51]),
        ],
    )
    def test_turn_or_river(self, board_parser: BoardParser, string: str, expected: int) -> None:
        """Test case to check if the board string is parsed correctly.

        Args:
            board_parser (BoardParser): The BoardParser instance.
            string (str): The input board string.
            expected (int): The expected parsed result.
        """
        assert board_parser.parse(string) == expected


class TestExceptionSuite:
    """Test suite for exceptional scenarios.

    Test Methods:
        - test_parse_board_str_invalid_type: ...
        - test_parse_board_str_invalid_length: ...
    """

    @pytest.mark.parametrize("string", [{}, 1, None])
    def test_parse_board_str_invalid_type(self, board_parser: BoardParser, string: str) -> None:
        """Test case to check if a TypeError is raised when a board string is not str type.

        Args:
            board_parser (BoardParser): The BoardParser instance.
            string (str): The input board string.
        """
        with pytest.raises(TypeError):
            board_parser.parse(string)

    @pytest.mark.parametrize("string", ["", "A", "AdAc", "AhKdJsQc", "AsKsQsJsTs"])
    def test_parse_board_str_invalid_length(self, board_parser: BoardParser, string: str) -> None:
        """Test case to check if a ValueError is raised when a board string has an invalid length.

        Args:
            board_parser (BoardParser): The BoardParser instance.
            string (str): The input board string.
        """
        with pytest.raises(ValueError):
            board_parser.parse(string)

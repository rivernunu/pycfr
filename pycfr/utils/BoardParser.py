from collections.abc import Iterator

from pycfr.utils.CardParser import CardParser


class BoardParser:
    """A class for parsing board strings into a list of integers.

    The board string can represent either a single card or a flop of three cards.

    Example:
        >>> board_parser = BoardParser()
        >>> board_parser.parse("3d")
        5
        >>> board_parser.parse("2c3d4h")
        [0, 5, 10]
    """

    def parse(self, string: str) -> list[int] | int:
        """Parse the board string into a list of integers representing the cards.

        Args:
            string (str): The input board string to be parsed.

        Returns:
            Union[int, list[int]]:
                If the length of the input string is 2, returns the parsed card as an integer.
                If the length of the input string is 6, returns a sorted list of three cards as integers.

        Raises:
            TypeError: If the input string is not of type str.
            ValueError: If the length of the input string is neither 2 nor 6.
        """
        if not isinstance(string, str):
            raise TypeError(f"Cards must be a string type. {string}")
        if len(string) == 2:
            return self._card_from_str(string)
        elif len(string) == 6:
            return self._flop_from_str(string)
        else:
            raise ValueError(f"Cards length must be 2 or 6. {string}")

    def _flop_from_str(self, string: str) -> list[int]:
        """Parse a flop string into a sorted list of three cards as integers.

        Args:
            string (str): The input flop string to be parsed.

        Returns:
            list[int]: A sorted list of three cards as integers.

        Raises:
            ValueError: If the input string does not contain unique cards.
        """
        result: list[int] = [0] * 3
        chars: Iterator[str] = iter(string)

        result[0] = self._card_from_chars(chars)
        result[1] = self._card_from_chars(chars)
        result[2] = self._card_from_chars(chars)

        if (result[0] == result[1]) or (result[1] == result[2]):
            raise ValueError(f"Cards must be unique. {string}")

        result.sort()

        return result

    def _card_from_str(self, string: str) -> int:
        """Parse a card string into an integer representation.

        Args:
            string (str): The input card string to be parsed.

        Returns:
            int: The parsed card as an integer.
        """
        chars = iter(string)
        result = self._card_from_chars(chars)

        return result

    def _card_from_chars(self, chars: Iterator[str]) -> int:
        """Parse two characters representing a rank and a suit into a card integer.

        Args:
            chars (Iterator[str]): An iterator over the characters representing a rank and a suit.

        Returns:
            int: The parsed card as an integer.
        """
        rank_char = next(chars)
        suit_char = next(chars)

        rank = CardParser.char_to_rank(rank_char)
        suit = CardParser.char_to_suit(suit_char)

        return (rank << 2) | suit

from dataclasses import dataclass

from src.models.BetSize import BetSize


@dataclass
class BetSizeCandidates:
    list_bet_size: list[BetSize]
    list_raise_size: list[BetSize]

    def try_form(bet_size_str: str, raise_size_str: str) -> None:
        
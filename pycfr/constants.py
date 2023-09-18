"""constants.py.

This module contains constants used throughout the project.
"""
from typing import Final

NOT_DEALT: Final[int] = 0b11111111
PLAYER_OOP: Final[int] = 0
PLAYER_IP: Final[int] = 1
PLAYER_CHANCE: Final[int] = 2
PLAYER_MASK: Final[int] = 3
PLAYER_CHANCE_FLAG: Final[int] = 4
PLAYER_TERMINAL_FLAG: Final[int] = 0b1000
PLAYER_FOLD_FLAG: Final[int] = 0b00011000

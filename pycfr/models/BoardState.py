from enum import IntEnum


class BoardState(IntEnum):
    Flop: int = 0
    Turn: int = 1
    River: int = 2

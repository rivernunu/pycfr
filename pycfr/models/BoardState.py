"""test.

>>> BoardState(Flop)
aaa

"""

from enum import IntEnum


class BoardState(IntEnum):
    """Enumeration of BoardState.

    Attributes:
        Flop (int): 0.
        Turn (int): 1.
        River (int): 2.

    Example:
        >>> BoardState
        <enum 'BoardState'>
        >>> BoardState.Flop
        <BoardState.Flop: 0>
        >>> BoardState.Turn
        <BoardState.Turn: 1>
        >>> BoardState.River
        <BoardState.River: 2>
        >>> BoardState.Flop == 0
        True
    """

    Flop: int = 0
    Turn: int = 1
    River: int = 2

from enum import IntEnum


class State(IntEnum):
    ConfigError: int = 0
    Uninitialized: int = 1
    TreeBuilt: int = 2
    MemoryAllocated: int = 3
    Solved: int = 4

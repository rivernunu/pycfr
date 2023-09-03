from dataclasses import dataclass


@dataclass
class BuildTreeInfo:
    flop_idx: int
    turn_idx: int
    river_idx: int
    num_storage: int
    num_storage_ip: int
    num_storage_chance: int

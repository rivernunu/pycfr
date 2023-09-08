from dataclasses import dataclass, field
from pycfr.utils.RangeParser import RangeParser


@dataclass
class Range:
    range_string_representation: str = ""
    range_list_float_representation: list[float] = field(default_factory=lambda: [0.0] * 1326)

    def __post_init__(self) -> None:
        self.range_list_float_representation = RangeParser.from_sanitized_str(
            self.range_string_representation
        )

    def ones(self) -> None:
        self.data = [1.0] * int(52 * 51 / 2)

    def clear(self) -> None:
        self.data = [0.0] * int(52 * 51 / 2)

    def check_weight(self, weight: float) -> bool:
        if 0.0 <= weight <= 1.0:
            return True
        else:
            raise ValueError

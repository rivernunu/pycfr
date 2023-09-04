from dataclasses import dataclass


@dataclass
class Range:
    data: list[float] = [0.0] * int(52 * 51 / 2)

    def ones(self) -> None:
        self.data = [1.0] * int(52 * 51 / 2)

    def clear(self) -> None:
        self.data = [0.0] * int(52 * 51 / 2)

    def check_weight(self, weight: float) -> bool:
        if 0.0 <= weight <= 1.0:
            return True
        else:
            raise ValueError

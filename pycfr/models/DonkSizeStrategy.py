"""donk_size_strategy.

Example:
>>> donk_sizes = DonkSizeStrategy(donk_str="60%,e,a")
>>> donk_sizes
DonkSizeStrategy(donk_strategy=[BetSize(type=<BetSizeType.PotRelative: 'PotRelative'>, value=60.0), BetSize(type=<BetSizeType.Geometric: 'Geometric'>, value=(0, inf)), BetSize(type=<BetSizeType.AllIn: 'AllIn'>, value=0)])
>>> donk_sizes.donk_strategy[0].type
<BetSizeType.PotRelative: 'PotRelative'>
>>> donk_sizes.donk_strategy[0].value
60.0
"""
import sys
from dataclasses import dataclass, field

from pycfr.models.BetSize import BetSize, BetSizeType


@dataclass
class DonkSizeStrategy:
    donk_strategy: list[BetSize] = field(default_factory=list)

    def __init__(self, donk_str: str) -> None:
        """Initializes a new instance of the DonkSizeCandidates class.

        Args:
            donk_str (str): A comma-separated string representing the bet sizes.
        """
        self.donk_strategy = []
        donk_sizes = donk_str.split(",")

        for donk in donk_sizes:
            self.donk_strategy.append(self.parse(donk, False))

    def parse(self, string: str, is_raise: bool) -> BetSize:
        """Parses a string representation of a bet size and returns a BetSize object.

        Args:
            string (str): The string representation of the bet size.
            is_raise (bool): A flag indicating whether the bet size is for a raise or not.

        Returns:
            BetSize: The parsed bet size represented as a BetSize object.

        Raises:
            ValueError: If the string does not match any of the supported bet size formats.

        Example:
            bet_size_candidates = BetSizeCandidates("2x,3c,4e,5%,a", "6x,7c,8e,9%,a")
            bet_size = bet_size_candidates.parse("2x", True)
            print(bet_size)
        """
        if string.endswith("x"):
            if not is_raise:
                raise ValueError
            return self.parse_times(string)

        elif string.endswith("c"):
            return self.parse_chip(string)
        elif "e" in string:
            return self.parse_geometric(string)
        elif string.endswith("%"):
            return self.parse_percent(string)
        elif string == "a":
            return self.parse_allin(string)
        else:
            raise ValueError

    def parse_times(self, string: str) -> BetSize:
        suffix = "x"
        string_splitted = string.split(suffix)
        times_str = string_splitted[0]

        time_float = float(times_str)

        if time_float < 1.0:
            raise ValueError

        return BetSize(type=BetSizeType.PrevBetRelative, value=time_float)

    def parse_chip(self, string: str) -> BetSize:
        suffix = "c"
        string_splitted = string.split(suffix)
        add_str = string_splitted[0]

        add = float(add_str)
        if int(add) != add:
            raise ValueError(f"Additional size must be an integer. {add_str}")
        if add > float(sys.maxsize):
            raise ValueError(f"Additional size must be less than 2^63 - 1. {add_str}")

        return BetSize(type=BetSizeType.Additive, value=int(add))

    def parse_geometric(self, string: str) -> BetSize:
        suffix = "e"
        string_splitted = string.split(suffix)
        num_streets_str = string_splitted[0]
        max_pot_rel_str = string_splitted[1]

        if not num_streets_str:
            num_streets = 0
        else:
            float_val = float(num_streets_str)
            if int(float_val) != float_val or float_val == 0.0:
                raise ValueError(
                    f"Number og streets must be a positive integer. {num_streets_str}"
                )
            elif float_val > 100.0:
                raise ValueError(
                    f"Number of streets must be less than or equal to 100. {num_streets_str}"
                )
            num_streets = int(float_val)

        if not max_pot_rel_str:
            max_pot_rel = float("inf")
        else:
            max_pot_rel_str = max_pot_rel_str.rstrip("%")
            max_pot_rel = float(max_pot_rel_str) / 100.0

        if len(string_splitted) > 2:
            raise ValueError

        return BetSize(type=BetSizeType.Geometric, value=(num_streets, max_pot_rel))

    def parse_percent(self, string: str) -> BetSize:
        """X%形式の処理.

        例: "75%", "150%"
        """
        suffix = "%"
        value = float(string.rstrip(suffix))
        return BetSize(type=BetSizeType.PotRelative, value=value)

    def parse_allin(self, string: str) -> BetSize:
        return BetSize(type=BetSizeType.AllIn, value=0)

"""main module.

```console
python -m pycfr
```

"""
from pycfr.constants import NOT_DEALT
from pycfr.models.ActionTree import ActionTree
from pycfr.models.BetSizeStrategy import BetSizeStrategy
from pycfr.models.BoardState import BoardState
from pycfr.models.CardConfig import CardConfig
from pycfr.models.DonkSizeStrategy import DonkSizeStrategy
# from pycfr.models.Game import Game
from pycfr.models.Range import Range
from pycfr.models.TreeConfig import TreeConfig
from pycfr.utils.BoardParser import BoardParser


def main() -> None:
    oop_range: str = "2c2d:1.0"
    ip_range: str = "AsAd:1.0"
    range_oop = Range(range_string_representation=oop_range)
    range_ip = Range(range_string_representation=ip_range)

    card_config = CardConfig(
        each_range=(range_oop, range_ip),
        flop=BoardParser.parse("Td9d6h"),
        turn=BoardParser.parse("Qc"),
        river=[NOT_DEALT],
    )

    bet_sizes = BetSizeStrategy(bet_str="60%,e,a", raise_str="2.5x")
    donk_sizes = DonkSizeStrategy(donk_str="60%,e,a")

    tree_config = TreeConfig(
        initial_state=BoardState.Turn,
        starting_pot=200,
        effective_stack=[900, 900],
        rake_rate=0.0,
        rake_cap=0.0,
        flop_bet_sizes=[bet_sizes, bet_sizes],
        turn_bet_sizes=[bet_sizes, bet_sizes],
        river_bet_sizes=[bet_sizes, bet_sizes],
        turn_donk_sizes=donk_sizes,
        river_donk_sizes=donk_sizes,
        add_allin_threshold=1.5,
        force_allin_threshold=0.15,
        merging_threshold=0.1,
    )

    action_tree = ActionTree(config=tree_config)


if __name__ == "__main__":
    main()

from constants import NOT_DEALT
from models.CardConfig import CardConfig
from models.Range import Range


def main() -> None:
    oop_range: str = "AKs,22"
    # ip_range: str = ...
    range_oop = Range(oop_range)
    print(range_oop)
    """
    card_config = CardConfig(
        range_ = Range(oop_range), Range(ip_range)
        flop = flop_from_str("Td9d6h")
        turn = card_from_str("Qc")
        river = NOT_DEALT
    )
    """


if __name__ == "__main__":
    main()

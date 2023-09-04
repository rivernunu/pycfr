class CardParser:
    _rank_map: dict[str, int] = {
        "A": 12,
        "a": 12,
        "K": 11,
        "k": 11,
        "Q": 10,
        "q": 10,
        "J": 9,
        "j": 9,
        "T": 8,
        "t": 8,
        "9": 7,
        "8": 6,
        "7": 5,
        "6": 4,
        "5": 3,
        "4": 2,
        "3": 1,
        "2": 0,
    }
    _suit_map: dict[str, int] = {"c": 0, "d": 1, "h": 2, "s": 3}

    @classmethod
    def char_to_rank(cls, rank_str: str) -> int:
        if rank_str in cls._rank_map:
            return cls._rank_map[rank_str]
        else:
            raise ValueError(f"Expected rank character: {rank_str}")

    @classmethod
    def char_to_suit(cls, suit_str: str) -> int:
        if suit_str in cls._suit_map:
            return cls._suit_map[suit_str]
        else:
            raise ValueError(f"Expected suit character: {suit_str}")

    @staticmethod
    def card_pair_to_index(card1: int, card2: int) -> int:
        if card1 > card2:
            card1, card2 = card2, card1
        return card1 * (101 - card1) // 2 + card2 - 1

    @staticmethod
    def index_to_card_pair(index: int) -> tuple[int, int]:
        ...

"""Pytest::Unit test of CardIndex."""
import pytest

from pycfr.models.Suitedness import Suitedness, SuitednessType
from pycfr.utils.RangeIndex import RangeIndex


class TestNormalSuite:
    """ """

    @pytest.mark.parametrize(
        ["rank1", "rank2", "expected"],
        [
            (0, 0, [0, 1, 2, 51, 52, 101]),
            (1, 1, [198, 199, 200, 245, 246, 291]),
            (2, 2, [380, 381, 382, 423, 424, 465]),
            (3, 3, [546, 547, 548, 585, 586, 623]),
            (4, 4, [696, 697, 698, 731, 732, 765]),
            (5, 5, [830, 831, 832, 861, 862, 891]),
            (6, 6, [948, 949, 950, 975, 976, 1001]),
            (7, 7, [1050, 1051, 1052, 1073, 1074, 1095]),
            (8, 8, [1136, 1137, 1138, 1155, 1156, 1173]),
            (9, 9, [1206, 1207, 1208, 1221, 1222, 1235]),
            (10, 10, [1260, 1261, 1262, 1271, 1272, 1281]),
            (11, 11, [1298, 1299, 1300, 1305, 1306, 1311]),
            (12, 12, [1320, 1321, 1322, 1323, 1324, 1325]),
        ],
    )
    def test_pocket_pairs_suit_all(self, rank1: int, rank2: int, expected: list[int]) -> None:
        suitedness = Suitedness(SuitednessType.All)
        result = RangeIndex.extract(rank1, rank2, suitedness)
        assert result == expected

    @pytest.mark.parametrize(
        ["rank1", "rank2", "expected"],
        [
            (0, 0, [0]),
            (1, 1, [198]),
            (2, 2, [380]),
            (3, 3, [546]),
            (4, 4, [696]),
            (5, 5, [830]),
            (6, 6, [948]),
            (7, 7, [1050]),
            (8, 8, [1136]),
            (9, 9, [1206]),
            (10, 10, [1260]),
            (11, 11, [1298]),
            (12, 12, [1320]),
        ],
    )
    def test_pocket_pairs_suit_club_dia(self, rank1: int, rank2: int, expected: list[int]) -> None:
        suitedness = Suitedness(SuitednessType.Specific, (0, 1))
        result = RangeIndex.extract(rank1, rank2, suitedness)
        assert result == expected

    @pytest.mark.parametrize(
        ["rank1", "rank2", "expected"],
        [
            (0, 0, [0]),
            (1, 1, [198]),
            (2, 2, [380]),
            (3, 3, [546]),
            (4, 4, [696]),
            (5, 5, [830]),
            (6, 6, [948]),
            (7, 7, [1050]),
            (8, 8, [1136]),
            (9, 9, [1206]),
            (10, 10, [1260]),
            (11, 11, [1298]),
            (12, 12, [1320]),
        ],
    )
    def test_pocket_pairs_suit_dia_club(self, rank1: int, rank2: int, expected: list[int]) -> None:
        suitedness = Suitedness(SuitednessType.Specific, (0, 1))
        result = RangeIndex.extract(rank1, rank2, suitedness)
        assert result == expected

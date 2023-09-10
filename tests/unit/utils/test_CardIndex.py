"""Pytest::Unit test of CardIndex."""
import pytest

from pycfr.models.Suitedness import Suitedness, SuitednessType
from pycfr.utils.RangeIndex import RangeIndex


class TestNormalPocketPairs:
    """Pocket Pairs Normal Test Cases.

    Methods:
        test_pocket_pairs_suit_all: `22`, `33`, … `AA`.
        test_pocket_pairs_suit_club_dia: `2c2d`, `3c3d`, …. `AcAd`.
        test_pocket_pairs_suit_club_heart: `2c2h`, `3c3h`, …, `AcAh`.
        test_pocket_pairs_suit_club_spade: `2c2s`, `3c3s`, …, `AcAs`.
        test_pocket_pairs_suit_dia_heart: `2d2h`, `3d3h`, …, `AdAh`.
        test_pocket_pairs_suit_dia_spade: `2d2s`, `3d3s`, …, `AdAs`.
        test_pocket_pairs_suit_heart_spade: `2h2s`, `3h3s`, …, `AhAs`.

        test_pocket_pairs_suit_dia_club: `2d2c`, `3d3c`, …, `AdAc`.
        test_pocket_pairs_suit_heart_club: `2h2c`, `3h3c`, …, `AhAc`.
    """

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
            (0, 0, [1]),
            (1, 1, [199]),
            (2, 2, [381]),
            (3, 3, [547]),
            (4, 4, [697]),
            (5, 5, [831]),
            (6, 6, [949]),
            (7, 7, [1051]),
            (8, 8, [1137]),
            (9, 9, [1207]),
            (10, 10, [1261]),
            (11, 11, [1299]),
            (12, 12, [1321]),
        ],
    )
    def test_pocket_pairs_suit_club_heart(
        self, rank1: int, rank2: int, expected: list[int]
    ) -> None:
        suitedness = Suitedness(SuitednessType.Specific, (0, 2))
        result = RangeIndex.extract(rank1, rank2, suitedness)
        assert result == expected

    @pytest.mark.parametrize(
        ["rank1", "rank2", "expected"],
        [
            (0, 0, [2]),
            (1, 1, [200]),
            (2, 2, [382]),
            (3, 3, [548]),
            (4, 4, [698]),
            (5, 5, [832]),
            (6, 6, [950]),
            (7, 7, [1052]),
            (8, 8, [1138]),
            (9, 9, [1208]),
            (10, 10, [1262]),
            (11, 11, [1300]),
            (12, 12, [1322]),
        ],
    )
    def test_pocket_pairs_suit_club_spade(
        self, rank1: int, rank2: int, expected: list[int]
    ) -> None:
        suitedness = Suitedness(SuitednessType.Specific, (0, 3))
        result = RangeIndex.extract(rank1, rank2, suitedness)
        assert result == expected

    @pytest.mark.parametrize(
        ["rank1", "rank2", "expected"],
        [
            (0, 0, [51]),
            (1, 1, [245]),
            (2, 2, [423]),
            (3, 3, [585]),
            (4, 4, [731]),
            (5, 5, [861]),
            (6, 6, [975]),
            (7, 7, [1073]),
            (8, 8, [1155]),
            (9, 9, [1221]),
            (10, 10, [1271]),
            (11, 11, [1305]),
            (12, 12, [1323]),
        ],
    )
    def test_pocket_pairs_suit_dia_heart(
        self, rank1: int, rank2: int, expected: list[int]
    ) -> None:
        suitedness = Suitedness(SuitednessType.Specific, (1, 2))
        result = RangeIndex.extract(rank1, rank2, suitedness)
        assert result == expected

    @pytest.mark.parametrize(
        ["rank1", "rank2", "expected"],
        [
            (0, 0, [52]),
            (1, 1, [246]),
            (2, 2, [424]),
            (3, 3, [586]),
            (4, 4, [732]),
            (5, 5, [862]),
            (6, 6, [976]),
            (7, 7, [1074]),
            (8, 8, [1156]),
            (9, 9, [1222]),
            (10, 10, [1272]),
            (11, 11, [1306]),
            (12, 12, [1324]),
        ],
    )
    def test_pocket_pairs_suit_dia_spade(
        self, rank1: int, rank2: int, expected: list[int]
    ) -> None:
        suitedness = Suitedness(SuitednessType.Specific, (1, 3))
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
        suitedness = Suitedness(SuitednessType.Specific, (1, 0))
        result = RangeIndex.extract(rank1, rank2, suitedness)
        assert result == expected

    @pytest.mark.parametrize(
        ["rank1", "rank2", "expected"],
        [
            (0, 0, [1]),
            (1, 1, [199]),
            (2, 2, [381]),
            (3, 3, [547]),
            (4, 4, [697]),
            (5, 5, [831]),
            (6, 6, [949]),
            (7, 7, [1051]),
            (8, 8, [1137]),
            (9, 9, [1207]),
            (10, 10, [1261]),
            (11, 11, [1299]),
            (12, 12, [1321]),
        ],
    )
    def test_pocket_pairs_suit_heart_club(
        self, rank1: int, rank2: int, expected: list[int]
    ) -> None:
        suitedness = Suitedness(SuitednessType.Specific, (2, 0))
        result = RangeIndex.extract(rank1, rank2, suitedness)
        assert result == expected


class TestNormalSuited:
    @pytest.mark.parametrize(
        ["rank1", "rank2", "expected"],
        [
            (12, 11, [1301, 1308, 1314, 1319]),
            (12, 10, [1267, 1278, 1288, 1297]),
            (12, 9, [1217, 1232, 1246, 1259]),
            (12, 8, [1151, 1170, 1188, 1205]),
            (12, 7, [1069, 1092, 1114, 1135]),
            (12, 6, [971, 998, 1024, 1049]),
            (12, 5, [857, 888, 918, 947]),
            (12, 4, [727, 762, 796, 829]),
            (12, 3, [581, 620, 658, 695]),
            (12, 2, [419, 462, 504, 545]),
            (12, 1, [241, 288, 334, 379]),
            (12, 0, [47, 98, 148, 197]),
        ],
    )
    def test_suited_ax_s(self, rank1: int, rank2: int, expected: list[int]) -> None:
        suitedness = Suitedness(SuitednessType.Suited)
        result = RangeIndex.extract(rank1, rank2, suitedness)
        assert result == expected


class TestNormalOffSuited:
    @pytest.mark.parametrize(
        ["rank1", "rank2", "expected"],
        [
            (
                12,
                11,
                [1302, 1303, 1304, 1307, 1309, 1310, 1312, 1313, 1315, 1316, 1317, 1318],
            ),
        ],
    )
    def test_suited_ax_o(self, rank1: int, rank2: int, expected: list[int]) -> None:
        suitedness = Suitedness(SuitednessType.Offsuit)
        result = RangeIndex.extract(rank1, rank2, suitedness)
        assert set(result) == set(expected)

"""Pytest::Unit test of CardIndex."""
import pytest

from pycfr.models.Suitedness import Suitedness
from pycfr.utils.RangeIndex import RangeIndex


class TestNormalSuite:
    """ """

    def test_001(self) -> None:
        rank1 = 0
        rank2 = 0
        suitedness = Suitedness(Specific=(0, 1))
        result = RangeIndex.extract(rank1, rank2, suitedness)
        excepted = [0]

        assert result == excepted

    def test_pocket_pairs(self) -> None:
        rank1 = 3
        rank2 = 3
        suitedness = Suitedness(All=True)
        result = RangeIndex.extract(rank1, rank2, suitedness)
        excepted = [0]

        assert result == excepted

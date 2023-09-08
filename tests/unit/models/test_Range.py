"""PyTest:: Unit test of Range

Test Suites:
    - ...
    - ...

Fixtures:
    - ...
"""
import pytest

from pycfr.models.Range import Range


@pytest.fixture
def data() -> list[float]:
    """Fixture that returns a list of floats.

    A list of floats with a length of 1326,
    where each element is initialized to 0.0.
    """
    data = [0.0] * 1326
    return data


class TestNormalSuite:
    """Test suite for normal execution scenarios.

    Test Methods:
        - ...:
        - ...:
    """

    def test_001(self, data: list[float]) -> None:
        range_str = "2c2d:1.0"
        data[0] = 1.0
        expected = data
        range_ = Range(range_string_representation=range_str)

        assert range_.range_list_float_representation == expected

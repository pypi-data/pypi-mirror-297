"""A conventional beamformer library."""

import math

from hypothesis import given
from hypothesis.strategies import floats


def add(left: float, right: float) -> float:
    """Get the sum of two values (left, right)."""
    return left + right


@given(floats(), floats())
def test_add_should_be_commutative(left: float, right: float) -> None:
    """
    Test that the `add` function is commutative.

    This property-based test ensures that for any two floats,
    the order of addition doesn't affect the result.
    """
    left_sum = add(left, right)
    right_sum = add(right, left)

    if math.isnan(left_sum) or math.isnan(right_sum):
        assert math.isnan(right_sum)
        assert math.isnan(left_sum)
    else:
        assert add(left, right) == add(right, left)

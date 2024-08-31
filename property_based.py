from hypothesis import given
from hypothesis.strategies import floats, integers


def divide(x, y):
    return x / y


@given(integers(), integers())
def test_divide(x, y):
    assert divide(x, y) < x

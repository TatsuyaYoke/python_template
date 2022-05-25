import pytest

from main import add


@pytest.mark.parametrize(("x", "y", "correct"), [(1, 1, 2), (5, -1, 4)])
def test_add(x: int, y: int, correct: int) -> None:
    """
    Test addition result
    Parameters
    ----------
    x : int
    y : int
    correct : int
    """
    assert add(x, y) == correct

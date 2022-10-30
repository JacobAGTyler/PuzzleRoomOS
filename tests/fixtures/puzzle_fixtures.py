import pytest

from game.Puzzle import Puzzle


@pytest.fixture
def built_puzzle():
    return Puzzle("test_puzzle_1")

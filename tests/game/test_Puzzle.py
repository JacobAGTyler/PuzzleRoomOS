import pytest

from game.Puzzle import Puzzle


@pytest.fixture
def puzzle():
    return Puzzle("test_puzzle_1")


class TestPuzzle:
    def test_create_puzzle(self, puzzle):
        assert puzzle is not None
        assert isinstance(puzzle, Puzzle)

    def test_get_puzzle_id(self, puzzle):
        assert puzzle.get_puzzle_id() == "test_puzzle_1"

    def test_set_prerequisites(self, puzzle):
        assert puzzle.get_prerequisites() is None

        puzzle.set_prerequisites({"test_puzzle_2", "test_puzzle_3"})

        assert puzzle.get_prerequisites() is not None
        assert len(puzzle.get_prerequisites()) == 2
        assert "test_puzzle_2" in puzzle.get_prerequisites()

    def test_add_first_prerequisite(self, puzzle):
        assert puzzle.get_prerequisites() is None

        puzzle.add_prerequisite("test_puzzle_2")

        assert puzzle.get_prerequisites() is not None
        assert len(puzzle.get_prerequisites()) == 1
        assert "test_puzzle_2" in puzzle.get_prerequisites()

    def test_add_prerequisite(self, puzzle):
        assert puzzle.get_prerequisites() is None

        puzzle.add_prerequisite("test_puzzle_2")

        assert puzzle.get_prerequisites() is not None
        assert len(puzzle.get_prerequisites()) == 1
        assert "test_puzzle_2" in puzzle.get_prerequisites()

        puzzle.add_prerequisite("test_puzzle_3")

        assert puzzle.get_prerequisites() is not None
        assert len(puzzle.get_prerequisites()) == 2
        assert "test_puzzle_3" in puzzle.get_prerequisites()

    def test_get_prerequisites(self, puzzle):
        puzzle.set_prerequisites({"test_puzzle_2", "test_puzzle_3"})

        assert puzzle.get_prerequisites() is not None
        assert len(puzzle.get_prerequisites()) == 2
        assert "test_puzzle_2" in puzzle.get_prerequisites()

    def test_has_prerequisites(self, puzzle) -> bool:
        assert puzzle.has_prerequisites() is False

        puzzle.set_prerequisites({"test_puzzle_2", "test_puzzle_3"})
        assert puzzle.has_prerequisites() is True

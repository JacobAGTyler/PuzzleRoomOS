import pytest

from game.PuzzleConfig import PuzzleConfig


class TestPuzzleConfig:
    def test_puzzle_config_init(self):
        puzzle_config = PuzzleConfig({'definition': {}, 'setup': {}})
        assert isinstance(puzzle_config, PuzzleConfig)

    def test_puzzle_config_init_fail(self):
        with pytest.raises(ValueError, match="Puzzle definition and setup are required attributes"):
            _ = PuzzleConfig({'definition': {}})

        with pytest.raises(ValueError, match="Puzzle definition and setup are required attributes"):
            _ = PuzzleConfig({'setup': {}})

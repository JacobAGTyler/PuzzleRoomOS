import pytest

from game.puzzle_config import PuzzleConfig


class TestPuzzleConfig:
    def test_puzzle_config_init(self):
        puzzle_config = PuzzleConfig('TestName', {'definition': {}}, {'setup': {}}, 'TestCode')
        assert isinstance(puzzle_config, PuzzleConfig)
        assert puzzle_config.get_reference() == 'TestName'

    def test_puzzle_config_init_fail(self):
        with pytest.raises(ValueError, match="Puzzle definition and setup are required attributes"):
            _ = PuzzleConfig('TestGame', {'definition': {}}, None)

        with pytest.raises(ValueError, match="Puzzle definition and setup are required attributes"):
            _ = PuzzleConfig('TestGame', None, {'setup': {}})

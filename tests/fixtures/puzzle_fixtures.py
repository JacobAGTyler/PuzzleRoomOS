import uuid
import pytest

from unittest.mock import Mock

from game.Puzzle import Puzzle
from game.PuzzleConfig import PuzzleConfig


pc1 = Mock(spec=PuzzleConfig)
pc2 = Mock(spec=PuzzleConfig)
pc3 = Mock(spec=PuzzleConfig)
pc4 = Mock(spec=PuzzleConfig)
pc5 = Mock(spec=PuzzleConfig)


@pytest.fixture
def built_puzzle():
    return Puzzle(
        puzzle_reference='test_puzzle_1',
        puzzle_id=uuid.uuid4(),
        puzzle_config=pc1
    )

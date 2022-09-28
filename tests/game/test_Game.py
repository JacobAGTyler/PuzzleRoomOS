import networkx as nx
import pytest

from unittest.mock import Mock

from game.GameConfig import GameConfig
from game.Game import Game
from game.Puzzle import Puzzle


@pytest.fixture
def mock_game_config():
    return Mock(spec=GameConfig)

@pytest.fixture
def mock_puzzle_list():
    return [
        Mock(spec=Puzzle, puzzle_id="puzzle_1", prerequisites=None),
        Mock(spec=Puzzle, puzzle_id="puzzle_2", prerequisites=None),
        Mock(spec=Puzzle, puzzle_id="puzzle_3", prerequisites=['puzzle_1', 'puzzle_2']),
        Mock(spec=Puzzle, puzzle_id="puzzle_4", prerequisites=['puzzle_3']),
    ]


class TestGame:
    def test_game_init(self, mock_game_config):
        game = Game("test_ref", mock_game_config)
        assert isinstance(game, Game)

    def test_game_init_fail_reference(self, mock_game_config):
        with pytest.raises(ValueError, match="Game reference cannot be empty & must be at least 5 characters long"):
            game = Game("", mock_game_config)

        with pytest.raises(ValueError, match="Game reference cannot be empty & must be at least 5 characters long"):
            game = Game("test", mock_game_config)

    def test_game_init_fail_config(self):
        with pytest.raises(ValueError, match="Game config cannot be empty & must be of type GameConfig"):
            game = Game("test_ref", "")

        with pytest.raises(ValueError, match="Game config cannot be empty & must be of type GameConfig"):
            game = Game("test_ref", "NOT EMPTY")

    def test_parse_puzzle_dependencies(self, mock_game_config, mock_puzzle_list):
        game = Game("test_ref", mock_game_config)
        game._puzzles = mock_puzzle_list

        dependencies = game.parse_puzzle_dependencies()
        assert dependencies.number_of_nodes() == 4
        assert nx.is_directed_acyclic_graph(dependencies)

    def test_ppd_fail_circular(self, mock_game_config, mock_puzzle_list):
        game = Game("test_ref", mock_game_config)
        mock_puzzle_list[0] = Mock(spec=Puzzle, puzzle_id="puzzle_1", prerequisites=['puzzle_4'])
        game._puzzles = mock_puzzle_list

        with pytest.raises(ValueError, match="Puzzle dependencies are not valid, there are circular dependencies"):
            game.parse_puzzle_dependencies()

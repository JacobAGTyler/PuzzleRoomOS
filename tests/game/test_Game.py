import networkx as nx
import pytest

from unittest.mock import Mock
from tests.fixtures import mock_game_config, mock_puzzle_list, built_game, mock_puzzle

from game.Game import Game
from game.Puzzle import Puzzle


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

    def test_ppd_fail_circular(self, built_game, mock_puzzle_list):
        mock_puzzle_list[0] = Mock(spec=Puzzle, _puzzle_id="puzzle_1", _prerequisites=['puzzle_4'],
                                   has_prerequisites=lambda: True, get_prerequisites=lambda: ['puzzle_4'],
                                   get_puzzle_id=lambda: "puzzle_1")
        built_game._puzzles = mock_puzzle_list

        with pytest.raises(ValueError, match="Puzzle dependencies are not valid, there are circular dependencies"):
            built_game.parse_puzzle_dependencies()

    def test_evaluate_puzzles(self, built_game, mock_puzzle_list):
        built_game._puzzles = mock_puzzle_list

        assert built_game.evaluate_puzzles() == set(mock_puzzle_list)

    def test_get_puzzle(self, built_game):
        puz1 = built_game.get_puzzle("puzzle_1")
        assert isinstance(puz1, Puzzle)
        assert puz1.get_puzzle_id() == "puzzle_1"

        puz4 = built_game.get_puzzle("puzzle_4")
        assert isinstance(puz4, Puzzle)
        assert puz4.get_puzzle_id() == "puzzle_4"

    def test_get_unknown_puzzle(self, built_game):
        assert built_game.get_puzzle("puzzle_5") is None

    def test_get_puzzles(self, built_game):
        assert built_game.get_puzzles() == set(built_game._puzzles)

    def test_add_puzzle(self, built_game, mock_puzzle):
        built_game.add_puzzle(mock_puzzle)
        assert mock_puzzle in built_game._puzzles

    def test_add_false_puzzle(self, built_game):
        with pytest.raises(ValueError, match="Puzzle cannot be empty & must be of type Puzzle"):
            built_game.add_puzzle("")

        with pytest.raises(ValueError, match="Puzzle cannot be empty & must be of type Puzzle"):
            built_game.add_puzzle("NOT EMPTY")

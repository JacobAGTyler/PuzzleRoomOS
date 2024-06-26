import pytest

from server.grapher import build_graph


class TestBuildGraph:
    def test_grapher_no_game(self):
        with pytest.raises(ValueError, match="Game cannot be empty & must be of type Game"):
            build_graph("")

        with pytest.raises(ValueError, match="Game cannot be empty & must be of type Game"):
            build_graph("NOT EMPTY")

    def test_grapher_no_puzzles(self, mock_game):
        mock_game.puzzles = set()
        with pytest.raises(ValueError, match="Game has no puzzles"):
            build_graph(mock_game)

        mock_game.puzzles = None
        with pytest.raises(ValueError, match="Game has no puzzles"):
            build_graph(mock_game)

    def test_grapher_valid(self, built_game):
        graph = build_graph(built_game)
        sort_a = 'graph LR\n"puzzle_3" --> "puzzle_4"\n"puzzle_1" --> "puzzle_3"\n"puzzle_2" --> "puzzle_3"'
        sort_b = 'graph LR\n"puzzle_1" --> "puzzle_3"\n"puzzle_2" --> "puzzle_3"\n"puzzle_3" --> "puzzle_4"'

        assert graph == sort_a or graph == sort_b


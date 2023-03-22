import markdown

from enum import Enum
from typing import Optional

from game.Puzzle import Puzzle
from game.Game import Game


class GraphDirection(Enum):
    LEFT_RIGHT = 'LR'
    RIGHT_LEFT = 'RL'
    TOP_BOTTOM = 'TB'
    BOTTOM_TOP = 'BT'


def build_graph(game: Game, direction: GraphDirection = GraphDirection.LEFT_RIGHT) -> Optional[str]:

    graph_text = f'graph {direction.value}'

    if not game or not isinstance(game, Game):
        raise ValueError("Game cannot be empty & must be of type Game")

    if game.get_puzzles() is None or game.get_puzzles() == set():
        raise ValueError("Game has no puzzles")

    game_graph = game.evaluate_puzzles()

    if type(game_graph) is not set:
        raise ValueError("Game graph is not a set")

    game_graph_node: Puzzle
    for game_graph_node in game_graph:
        if game_graph_node.has_prerequisites():
            for prerequisite in game_graph_node.get_prerequisites():
                graph_text += f'\n"{prerequisite}" --> "{game_graph_node.get_puzzle_ref()}"'

    return graph_text

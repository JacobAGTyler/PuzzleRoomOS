import networkx as nx

from typing import Optional
from datetime import datetime
from game.GameConfig import GameConfig


class Game:
    def __init__(self, game_reference: str, game_config: GameConfig):
        if not game_reference or len(game_reference) < 5:
            raise ValueError("Game reference cannot be empty & must be at least 5 characters long")

        if not game_config or not isinstance(game_config, GameConfig):
            raise ValueError("Game config cannot be empty & must be of type GameConfig")

        self._game_reference: str = game_reference

        self._puzzles = set()
        self._started = False
        self._start_time: Optional[datetime] = None

    def parse_puzzle_dependencies(self):
        puzzle_dependencies = nx.DiGraph()

        for puzzle in self._puzzles:
            if puzzle.prerequisites:
                for prerequisite in puzzle.prerequisites:
                    puzzle_dependencies.add_edge(prerequisite, puzzle.puzzle_id)

        if not nx.is_directed_acyclic_graph(puzzle_dependencies):
            raise ValueError("Puzzle dependencies are not valid, there are circular dependencies")

        return puzzle_dependencies

    def evaluate_puzzles(self):
        nx.topological_sort(self.parse_puzzle_dependencies())

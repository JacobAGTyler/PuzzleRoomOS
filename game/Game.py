import networkx as nx

from typing import Optional, Union
from datetime import datetime, timedelta

from game.GameConfig import GameConfig
from game.Puzzle import Puzzle


class Game:
    def __init__(
            self,
            game_reference: str,
            game_config: GameConfig,
            puzzles: Optional[list[Puzzle]] = None,
            started: bool = False,
            ended: bool = False,
            start_time: Optional[datetime] = None,
            end_time: Optional[datetime] = None,
            game_id: Optional[int] = None,
    ):
        if not game_reference or len(game_reference) < 5:
            raise ValueError("Game reference cannot be empty & must be at least 5 characters long")

        if not game_config or not isinstance(game_config, GameConfig):
            raise ValueError("Game config cannot be empty & must be of type GameConfig")

        self.game_id: int = game_id
        self._game_reference: str = game_reference
        self.game_config: GameConfig = game_config

        self.puzzles: list[Puzzle] = puzzles
        self._puzzle_set: set[Puzzle] = set(self.puzzles)

        self.started = started
        self.ended = ended
        self._start_time: Optional[datetime] = start_time
        self._end_time: Optional[datetime] = end_time

    def get_puzzle(self, puzzle_ref: str) -> Optional[Puzzle]:
        for puzzle in self._puzzle_set:
            if puzzle.get_puzzle_ref() == puzzle_ref:
                return puzzle

        return None

    def get_puzzles(self) -> list[Puzzle]:
        return self.puzzles

    def get_id(self) -> int:
        return self.game_id

    def get_puzzle_set(self) -> set[Puzzle]:
        return self._puzzle_set

    def get_target_time(self) -> datetime:
        if self._start_time is None:
            return datetime.now() + timedelta(minutes=self.game_config.duration_minutes)

        return self._start_time + timedelta(minutes=self.game_config.duration_minutes)

    def get_reference(self) -> str:
        return self._game_reference

    def get_puzzle_count(self) -> int:
        return len(self.puzzles)

    def add_puzzle(self, puzzle: Puzzle):
        if not isinstance(puzzle, Puzzle):
            raise ValueError("Puzzle cannot be empty & must be of type Puzzle")

        self._puzzle_set.add(puzzle)

        if puzzle not in self.puzzles:
            self.puzzles.append(puzzle)

    def start_game(self):
        if not self.started:
            self.started = True
            self._start_time = datetime.now()
            return True

        return False

    def end_game(self):
        if not self.ended and self.started:
            self.ended = True
            self._end_time = datetime.now()
            return True

        return False

    def evaluate_trigger(self, trigger: str) -> Union[bool, set[str]]:
        if not self.started:
            return False

        for puzzle in self.puzzles:
            if puzzle.evaluate_solution(trigger):
                return puzzle.get_triggers()

        return False

    def parse_puzzle_dependencies(self):
        puzzle_dependencies = nx.DiGraph()

        puzzle: Puzzle
        for puzzle in self._puzzle_set:
            if puzzle.has_prerequisites():
                for prerequisite in puzzle.get_prerequisites():
                    puzzle_dependencies.add_edge(prerequisite, puzzle.get_puzzle_ref())

        if not nx.is_directed_acyclic_graph(puzzle_dependencies):
            raise ValueError("Puzzle dependencies are not valid, there are circular dependencies")

        return puzzle_dependencies

    def evaluate_puzzles(self) -> set[Puzzle]:
        sorted_puzzles = nx.topological_sort(self.parse_puzzle_dependencies())
        sorted_puzzles = list(reversed(list(sorted_puzzles)))
        end_puzzles = set()

        for puzzle_id in sorted_puzzles:
            puzzle = self.get_puzzle(puzzle_id)
            end_puzzles.add(puzzle)

        return end_puzzles

    def to_dict(self) -> dict:
        return {
            'game_id': self.get_id(),
            'game_reference': self.get_reference(),
            'game_config': {
                'config_reference': self.game_config.get_reference(),
                'name': self.game_config.get_name(),
                'version': self.game_config.get_version()
            },
            'puzzles': [puzzle.to_dict() for puzzle in self.puzzles],
            'started': self.started,
            'ended': self.ended,
            'target_time': self.get_target_time().isoformat(),
            'start_time': self._start_time.isoformat() if self._start_time else None,
            'end_time': self._end_time.isoformat() if self._end_time else None,
        }

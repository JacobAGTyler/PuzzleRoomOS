import networkx as nx

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Table, ForeignKey

from typing import Optional
from datetime import datetime, timedelta
from game.GameConfig import GameConfig
from game.Puzzle import Puzzle

from data import mapper_registry

game_table = Table(
    'game',
    mapper_registry.metadata,

    Column('game_id', Integer, primary_key=True),
    Column('game_ref', String(255)),
    Column('game_config_id', Integer, ForeignKey('game_config.game_config_id')),
    Column('started', Boolean),
    Column('ended', Boolean),
    Column('start_time', DateTime, nullable=True),
    Column('end_time', DateTime, nullable=True),
)


class Game:
    def __init__(self, game_reference: str, game_config: GameConfig):
        if not game_reference or len(game_reference) < 5:
            raise ValueError("Game reference cannot be empty & must be at least 5 characters long")

        if not game_config or not isinstance(game_config, GameConfig):
            raise ValueError("Game config cannot be empty & must be of type GameConfig")

        self._game_reference: str = game_reference
        self._game_config: GameConfig = game_config

        self._puzzles: set[Puzzle] = set()
        self._started = False
        self._ended = False
        self._start_time: Optional[datetime] = None
        self._end_time: Optional[datetime] = None

        super().__init__()

    def get_puzzle(self, puzzle_id: str) -> Optional[Puzzle]:
        for puzzle in self._puzzles:
            if puzzle.get_puzzle_id() == puzzle_id:
                return puzzle

        return None

    def add_puzzle(self, puzzle: Puzzle):
        if not puzzle or not isinstance(puzzle, Puzzle):
            raise ValueError("Puzzle cannot be empty & must be of type Puzzle")

        self._puzzles.add(puzzle)

    def get_puzzles(self) -> set[Puzzle]:
        return self._puzzles

    def get_target_time(self) -> datetime:
        if self._start_time is None:
            return datetime.now() + timedelta(minutes=self._game_config.duration_minutes)

        return self._start_time + timedelta(minutes=self._game_config.duration_minutes)

    def parse_puzzle_dependencies(self):
        puzzle_dependencies = nx.DiGraph()

        puzzle: Puzzle
        for puzzle in self._puzzles:
            if puzzle.has_prerequisites():
                for prerequisite in puzzle.get_prerequisites():
                    puzzle_dependencies.add_edge(prerequisite, puzzle.get_puzzle_id())

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

    def get_reference(self) -> str:
        return self._game_reference

    def to_dict(self) -> dict:
        return {
            'game_reference': self._game_reference,
            'game_config': {
                'config_reference': self._game_config.get_reference(),
                'name': self._game_config.get_name(),
                'version': self._game_config.get_version()
            },
            'puzzles': [puzzle.to_dict() for puzzle in self._puzzles],
            'started': self._started,
            'ended': self._ended,
            'start_time': self._start_time.isoformat() if self._start_time else None,
            'end_time': self._end_time.isoformat() if self._start_time else None,
        }


mapper_registry.map_imperatively(Game, game_table, properties={
    'puzzles': relationship('Puzzle', back_populates="game"),
    'game_config': relationship(GameConfig, back_populates='games'),
    'events': relationship('Event', back_populates='game'),
})

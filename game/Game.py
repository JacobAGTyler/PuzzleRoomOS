import uuid

import networkx as nx

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Table, ForeignKey

from typing import Optional, Union
from datetime import datetime, timedelta

from data.database import retrieve_entity, get_connection
from game.GameConfig import GameConfig, import_game_config
from game.Puzzle import Puzzle

from data import mapper_registry
from game.PuzzleConfig import PuzzleConfig

game_table = Table(
    'game',
    mapper_registry.metadata,

    Column('game_id', Integer, primary_key=True),
    Column('game_reference', String(255), key='_game_reference'),
    Column('game_config_id', Integer, ForeignKey('game_config.game_config_id')),
    Column('started', Boolean),
    Column('ended', Boolean),
    Column('start_time', DateTime, nullable=True, key='_start_time'),
    Column('end_time', DateTime, nullable=True, key='_end_time'),
)


class Game:
    def __init__(self, game_reference: str, game_config: GameConfig):
        if not game_reference or len(game_reference) < 5:
            raise ValueError("Game reference cannot be empty & must be at least 5 characters long")

        if not game_config or not isinstance(game_config, GameConfig):
            raise ValueError("Game config cannot be empty & must be of type GameConfig")

        self._game_reference: str = game_reference
        self.game_config: GameConfig = game_config

        self.puzzles: list[Puzzle] = []
        self._puzzle_set: set[Puzzle] = set()

        self.started = False
        self.ended = False
        self._start_time: Optional[datetime] = None
        self._end_time: Optional[datetime] = None

    def get_puzzle(self, puzzle_ref: str) -> Optional[Puzzle]:
        for puzzle in self._puzzle_set:
            if puzzle.get_puzzle_ref() == puzzle_ref:
                return puzzle

        return None

    def add_puzzle(self, puzzle: Puzzle):
        if not isinstance(puzzle, Puzzle):
            raise ValueError("Puzzle cannot be empty & must be of type Puzzle")

        self._puzzle_set.add(puzzle)

        if puzzle not in self.puzzles:
            self.puzzles.append(puzzle)

    def get_puzzles(self) -> list[Puzzle]:
        return self.puzzles

    def start_game(self):
        if not self.started:
            self.started = True
            self._start_time = datetime.now()

    def end_game(self):
        if not self.ended and self.started:
            self.ended = True
            self._end_time = datetime.now()

    def get_puzzle_set(self) -> set[Puzzle]:
        return self._puzzle_set

    def get_target_time(self) -> datetime:
        if self._start_time is None:
            return datetime.now() + timedelta(minutes=self.game_config.duration_minutes)

        return self._start_time + timedelta(minutes=self.game_config.duration_minutes)

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

    def get_reference(self) -> str:
        return self._game_reference

    def to_dict(self) -> dict:
        return {
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


mapper_registry.map_imperatively(Game, game_table, properties={
    'puzzles': relationship('Puzzle', back_populates="game"),
    'game_config': relationship(GameConfig, back_populates='games'),
    'events': relationship('Event', back_populates='game'),
})


def make_new_game(game_config_code: Union[uuid.UUID, str]) -> Game:
    if type(game_config_code) == str:
        game_config: GameConfig = import_game_config(game_config_code)
    else:
        session = get_connection()
        game_config: GameConfig = retrieve_entity(game_config_code, GameConfig, session)

    game = Game(game_config.get_reference(), game_config)

    puzzle_config: PuzzleConfig
    for puzzle_config in game_config.get_puzzle_configs():
        puzzle = Puzzle(puzzle_config=puzzle_config, puzzle_reference=puzzle_config.get_reference())
        game.add_puzzle(puzzle)

    return game

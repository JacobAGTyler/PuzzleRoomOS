import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime, Boolean, JSON, UUID
from sqlalchemy.orm import relationship

from data import mapper_registry

from game import PuzzleConfig


class Puzzle:
    def __init__(self, puzzle_config: PuzzleConfig, puzzle_reference: str, puzzle_id: UUID = uuid.uuid4()):
        self._puzzle_id: UUID = puzzle_id
        self._puzzle_config: PuzzleConfig = puzzle_config
        self._puzzle_reference = puzzle_reference

        self._prerequisites: Optional[set[str]] = None

        self._data: Optional[dict] = None
        self._solve_time: Optional[datetime] = None
        self._solved: bool = False

    def get_puzzle_id(self) -> str:
        return self._puzzle_id

    def get_puzzle_ref(self) -> str:
        return self._puzzle_reference

    def set_prerequisites(self, prerequisites: set[str]):
        self._prerequisites = prerequisites

    def add_prerequisite(self, prerequisite: str):
        if self._prerequisites is None:
            self._prerequisites = set()

        self._prerequisites.add(prerequisite)

    def get_prerequisites(self) -> Optional[set[str]]:
        return self._prerequisites

    def has_prerequisites(self) -> bool:
        return self._prerequisites is not None and len(self._prerequisites) > 0

    def to_dict(self) -> dict:
        return {
            'puzzle_id': self._puzzle_id,
        }


puzzle_table = Table(
    'puzzle',
    mapper_registry.metadata,

    Column('puzzle_id', UUID, primary_key=True),
    Column('game_id', Integer, ForeignKey('game.game_id')),
    Column('puzzle_config_id', Integer, ForeignKey('puzzle_config.puzzle_config_id')),
    Column('puzzle_reference', String(255)),
    Column('solved', Boolean, default=False),
    Column('solve_time', DateTime, nullable=True),
    Column('data', JSON, nullable=True),
)

mapper_registry.map_imperatively(Puzzle, puzzle_table, properties={
    'game': relationship('Game', back_populates="puzzles"),
    'puzzle_config': relationship('PuzzleConfig', back_populates="puzzles")
})

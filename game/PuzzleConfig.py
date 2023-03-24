import uuid
from typing import Optional

from sqlalchemy import Column, Integer, String, Table, JSON, ForeignKey, UUID
from sqlalchemy.orm import relationship

from data import mapper_registry


class PuzzleConfig:
    def __init__(
            self,
            puzzle_reference: str,
            definition: dict,
            setup: dict,
            puzzle_code: str = 'DEFAULT'
    ):
        if definition is None or setup is None:
            raise ValueError('Puzzle definition and setup are required attributes')

        self.definition = definition
        self.setup = setup
        self._puzzle_reference = puzzle_reference

    def get_reference(self) -> str:
        return self._puzzle_reference


puzzle_config_table = Table(
    'puzzle_config',
    mapper_registry.metadata,

    Column('puzzle_config_id', Integer, primary_key=True),
    Column('puzzle_code', String(32), nullable=False, default='DEFAULT'),
    Column('game_config_id', Integer, ForeignKey('game_config.game_config_id')),
    Column('puzzle_reference', String(255), key='_puzzle_reference'),
    Column('definition', JSON),
    Column('setup', JSON),
)

mapper_registry.map_imperatively(PuzzleConfig, puzzle_config_table, properties={
    'game_config': relationship('GameConfig', back_populates="puzzle_configs"),
    'puzzles': relationship('Puzzle', back_populates="puzzle_config")
})

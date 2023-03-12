from sqlalchemy import Column, Integer, String, Table, JSON, ForeignKey
from sqlalchemy.orm import relationship

from data import mapper_registry


class PuzzleConfig:
    def __init__(self, puzzle_data: dict):
        if 'definition' not in puzzle_data.keys() or 'setup' not in puzzle_data.keys():
            raise ValueError('Puzzle definition and setup are required attributes')

        self._puzzle_data = puzzle_data
        # self._puzzle_name = puzzle_data['name']

        self.definition = puzzle_data['definition']
        self.setup = puzzle_data['setup']


puzzle_config_table = Table(
    'puzzle_config',
    mapper_registry.metadata,

    Column('puzzle_config_id', Integer, primary_key=True),
    Column('game_config_id', Integer, ForeignKey('game_config.game_config_id')),
    Column('puzzle_data', JSON),
    Column('puzzle_reference', String(255)),
    Column('definition', String(255)),
    Column('setup', JSON),
)

mapper_registry.map_imperatively(PuzzleConfig, puzzle_config_table, properties={
    'game_config': relationship('GameConfig', back_populates="puzzle_configs"),
    'puzzles': relationship('Puzzle', back_populates="puzzle_config")
})

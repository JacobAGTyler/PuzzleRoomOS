from sqlalchemy import Column, Integer, String, Table, JSON, ForeignKey
from sqlalchemy.orm import relationship

from data import mapper_registry

from game.puzzle_config import PuzzleConfig

# puzzle_config_table = Table(
#     'puzzle_config',
#     mapper_registry.metadata,
#
#     Column('puzzle_config_id', Integer, primary_key=True),
#     Column('puzzle_code', String(32), nullable=False, default='DEFAULT', key='_puzzle_code'),
#     Column('game_config_id', Integer, ForeignKey('game_config.game_config_id')),
#     Column('puzzle_reference', String(255), key='_puzzle_reference'),
#     Column('definition', JSON),
#     Column('setup', JSON),
# )
#
# mapper_registry.map_imperatively(PuzzleConfig, puzzle_config_table, properties={
#     'game_config': relationship('GameConfig', back_populates="puzzle_configs"),
#     'puzzles': relationship('Puzzle', back_populates="puzzle_config")
# })
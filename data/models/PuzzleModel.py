from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime, Boolean, JSON, UUID
from sqlalchemy.orm import relationship

from data import mapper_registry

from game.puzzle import Puzzle


puzzle_table = Table(
    'puzzle',
    mapper_registry.metadata,

    Column('puzzle_id', Integer, primary_key=True, key='puzzle_id'),
    Column('game_id', Integer, ForeignKey('game.game_id'), nullable=False, key='game_id'),
    Column('puzzle_config_id', Integer, ForeignKey('puzzle_config.puzzle_config_id'), nullable=False),
    Column('puzzle_reference', String(255), nullable=False, key='puzzle_reference'),
    Column('solved', Boolean, default=False, key='solved'),
    Column('solve_time', DateTime, nullable=True, key='solve_time'),
    Column('data', JSON, nullable=True, key='data'),
    Column('solutions', JSON, nullable=True, key='solutions'),
    Column('triggers', JSON, nullable=True, key='triggers'),
    Column('prerequisites', JSON, nullable=True, key='prerequisites'),
)

mapper_registry.map_imperatively(Puzzle, puzzle_table, properties={
    'game': relationship('Game', back_populates="puzzles"),
    'puzzle_config': relationship('PuzzleConfig', back_populates="puzzles")
})
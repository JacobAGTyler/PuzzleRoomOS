from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Table, JSON

from data import mapper_registry

from game.game_config import GameConfig


game_config_table = Table(
    'game_config',
    mapper_registry.metadata,

    Column('game_config_id', Integer, primary_key=True),
    Column('config_reference', String(255)),
    Column('name', String(255), key='_name'),
    Column('version', String(255), key='_version'),
    Column('description', String(255)),
    Column('author', String(255)),
    Column('author_url', String(255)),
    Column('game_license', String(255)),
    Column('game_url', String(255)),
    Column('parameters', JSON),
    Column('duration_minutes', Integer),
)

mapper_registry.map_imperatively(GameConfig, game_config_table, properties={
    'games': relationship('Game', back_populates="game_config"),
    'puzzle_configs': relationship('PuzzleConfig', back_populates="game_config"),
})

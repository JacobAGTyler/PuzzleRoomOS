from sqlalchemy import Column, Integer, String, DateTime, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship

from game.game import Game
from game.game_config import GameConfig

from data import mapper_registry


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

mapper_registry.map_imperatively(Game, game_table, properties={
    'puzzles': relationship('Puzzle', back_populates="game"),
    'game_config': relationship(GameConfig, back_populates='games'),
    'events': relationship('GameEvent', back_populates='game'),
})

import datetime
import uuid
from enum import Enum

from sqlalchemy import Column, Integer, UUID, DateTime, Table, ForeignKey, String, JSON
from sqlalchemy.orm import relationship

from game.Game import Game
from data import mapper_registry


event_table = Table(
    'event',
    mapper_registry.metadata,

    Column('event_id', UUID, primary_key=True),
    Column('game_id', Integer, ForeignKey('game.game_id'), nullable=False),
    Column('event_time', DateTime, nullable=False),
    Column('event_type', String(32), nullable=False),
    Column('event_data', JSON, nullable=True),
)


class EventType(Enum):
    GAME_START = 'GAME_START'
    GAME_END = 'GAME_END'
    PUZZLE_HINT = 'PUZZLE_HINT'
    PUZZLE_SOLVE = 'PUZZLE_SOLVE'


class Event:
    def __init__(self, game: Game, event_type: EventType, event_data: dict = None):
        self._event_id = uuid.uuid4()
        self._game = game
        self._event_time = datetime.datetime.now()

        if not event_type or not isinstance(event_type, EventType):
            raise ValueError("Event type cannot be empty & must be of type EventType")

        self._event_type = event_type

        if event_data is None:
            event_data = {}

        self._event_data = event_data


mapper_registry.map_imperatively(Event, event_table, properties={
    'game': relationship(Game, back_populates='events')
})

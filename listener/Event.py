import datetime
import json
import uuid
from enum import Enum

from kafka import KafkaProducer
from sqlalchemy import Column, Integer, UUID, DateTime, Table, ForeignKey, String, JSON
from sqlalchemy.orm import relationship

from game.Game import Game
from data import mapper_registry


event_table = Table(
    'event',
    mapper_registry.metadata,

    Column('event_id', UUID, primary_key=True),
    Column('game_id', Integer, ForeignKey('game.game_id'), nullable=True),
    Column('event_time', DateTime, nullable=False),
    Column('event_type', String(32), nullable=False),
    Column('event_data', JSON, nullable=True),
)


class EventType(Enum):
    GAME_INITIALISATION = 'GAME_INITIALISATION'
    DEVICE_INITIALISATION = 'DEVICE_INITIALISATION'
    INTERFACE_INITIALISATION = 'INTERFACE_INITIALISATION'

    GAME_START = 'GAME_START'
    GAME_END = 'GAME_END'

    PUZZLE_HINT = 'PUZZLE_HINT'
    PUZZLE_SOLVE = 'PUZZLE_SOLVE'


class Event:
    def __init__(
            self,
            event_type: EventType,
            game: Game = None,
            published: bool = False,
            event_data: dict = None,
            event_id: uuid.UUID = uuid.uuid4(),
            event_time: datetime.datetime = datetime.datetime.now()
    ):
        self._event_id = event_id
        self._event_time = event_time
        self._published = published
        self._game = game

        if not event_type or not isinstance(event_type, EventType):
            raise ValueError("Event type cannot be empty & must be of type EventType")

        self._event_type = event_type

        if event_data is None:
            event_data = {}

        self._event_data = event_data

        if 'description' not in self._event_data.keys() or self._event_data['description'] is None:
            self.description = f'{self._event_type.value}_{self._event_id}'
        else:
            self.description = self._event_data['description']

    def publish(self):
        if not self._published:
            producer = KafkaProducer(bootstrap_servers='kafka:9092')
            producer.send('events', json.dumps(self.to_dict()).encode('utf-8'))
            producer.flush()
            self._published = True

    def to_dict(self) -> dict:
        data = {
            'event_id': str(self._event_id),
            'event_time': self._event_time.isoformat(),
            'event_type': self._event_type.value,
            'event_data': self._event_data,
            'description': self.description
        }

        if isinstance(self._game, Game):
            data['game'] = self._game.to_dict()

        return data

    def get_type(self):
        return self._event_type


mapper_registry.map_imperatively(Event, event_table, properties={
    'game': relationship(Game, back_populates='events')
})

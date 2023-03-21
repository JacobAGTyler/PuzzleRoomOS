import datetime
import json
import uuid
from enum import Enum
from typing import Optional

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

    GAME_START = 'GAME_START'
    GAME_END = 'GAME_END'

    PUZZLE_HINT = 'PUZZLE_HINT'
    PUZZLE_SOLVE = 'PUZZLE_SOLVE'

    ATTEMPT = 'ATTEMPT'


class Event:
    def __init__(
            self,
            event_type: EventType,
            game: Game = None,
            published: bool = False,
            event_data: dict = None,
            event_id: uuid.UUID = uuid.uuid4(),
            event_time: datetime.datetime = datetime.datetime.now(),
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
            self.description = f'{self._event_type.value}>>{self._event_id}'
        else:
            self.description = self._event_data['description']

    def publish(self):
        if not self._published:
            producer = KafkaProducer(batch_size=0, value_serializer=encode_message_event)
            pending_message = producer.send(topic='events', value=self)
            if pending_message.is_done:
                self._published = True
            producer.flush()

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

    def get_trigger_value(self) -> Optional[str]:
        triggered_event_types = [EventType.PUZZLE_SOLVE, EventType.ATTEMPT]

        if 'trigger' in self._event_data.keys() and self._event_type in triggered_event_types:
            return self._event_data['trigger']

        return None

    def get_type(self):
        return self._event_type


def encode_message_event(event: Event) -> bytes:
    return json.dumps(event.to_dict()).encode('utf-8')


def decode_message_event(message: bytes) -> Event:
    data: dict = json.loads(message.decode('utf-8'))
    data.pop('description')
    data['event_type'] = EventType(data['event_type'])

    return Event(**data)


mapper_registry.map_imperatively(Event, event_table, properties={
    'game': relationship(Game, back_populates='events')
})

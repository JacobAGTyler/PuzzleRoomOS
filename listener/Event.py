import datetime
import json
import uuid
import enum
from typing import Optional

from kafka import KafkaProducer
from sqlalchemy import Column, Integer, UUID, DateTime, Table, ForeignKey, JSON, Boolean, Enum
from sqlalchemy.orm import relationship

from game.Game import Game
from data import mapper_registry


class EventType(enum.Enum):
    GAME_CREATION = 'GAME_CREATION'

    GAME_INITIALISATION = 'GAME_INITIALISATION'
    DEVICE_INITIALISATION = 'DEVICE_INITIALISATION'

    GAME_START = 'GAME_START'
    GAME_END = 'GAME_END'

    PUZZLE_HINT = 'PUZZLE_HINT'
    PUZZLE_SOLVE = 'PUZZLE_SOLVE'

    ATTEMPT = 'ATTEMPT'


event_table = Table(
    'event',
    mapper_registry.metadata,

    Column('event_id', UUID(as_uuid=False), primary_key=True, key='_event_id'),
    Column('game_id', Integer, ForeignKey('game.game_id'), nullable=True),
    Column('event_time', DateTime, nullable=False, key='_event_time'),
    Column('published', Boolean, nullable=False, default=False, key='_published'),
    Column('event_type', Enum(EventType), nullable=False, key='_event_type'),
    Column('event_data', JSON, nullable=True, key='_event_data'),
)


class Event:
    def __init__(
            self,
            event_type: EventType,
            game: Game = None,
            published: bool = False,
            event_data: Optional[dict] = None,
            event_id: uuid.UUID = uuid.uuid4(),
            event_time: datetime.datetime = datetime.datetime.now(),
    ):
        self._event_id = event_id
        self._event_time = event_time
        self._published = published
        self.game = game

        if not event_type or not isinstance(event_type, EventType):
            raise ValueError("Event type cannot be empty & must be of type EventType")

        self._event_type = event_type

        if event_data is None or not isinstance(event_data, dict):
            event_data = {}

        self._event_data = event_data

    def publish(self):
        if not self._published:
            producer = KafkaProducer(batch_size=0, value_serializer=encode_message_event)
            pending_message = producer.send(topic='events', value=self)
            producer.flush()
            if pending_message.is_done:
                self._published = True

    def is_published(self) -> bool:
        return self._published

    def to_dict(self) -> dict:
        data = {
            'event_id': str(self._event_id),
            'event_time': self._event_time.isoformat(),
            'event_type': self._event_type.value,
            'event_data': self._event_data
        }

        if isinstance(self.game, Game):
            data['game'] = self.game.to_dict()

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
    data['published'] = True
    if 'game' in data.keys():
        data.pop('game')
    data['event_type'] = EventType(data['event_type'])
    data['event_id'] = uuid.UUID(data['event_id'])

    return Event(**data)


mapper_registry.map_imperatively(Event, event_table, properties={
    'game': relationship(Game, back_populates='events')
})

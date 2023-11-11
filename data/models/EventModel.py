from sqlalchemy import Column, Integer, UUID, DateTime, Table, ForeignKey, JSON, Boolean, Enum
from sqlalchemy.orm import relationship

from data import mapper_registry

from game.game import Game
from listener.event import EventType, Event
from listener.game_event import GameEvent


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

mapper_registry.map_imperatively(GameEvent, event_table, properties={
    'game': relationship(Game, back_populates='events')
})

mapper_registry.map_imperatively(Event, event_table)

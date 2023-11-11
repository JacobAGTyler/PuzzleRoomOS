import json
import logging
import uuid

from kafka import KafkaConsumer
from sqlalchemy.orm import Session

from game.game import Game
from listener.device import Device
from listener.event import Event, EventType
from listener.game_event import GameEvent
from data.database import get_connection, get_engine, save_entity, retrieve_entity
from listener.game_handler import GameHandler


class DatabaseDevice(Device):
    def __init__(self, device_config: dict, device_code: str):
        super().__init__(device_config, device_code)
        self.session: Session = get_connection(engine=get_engine())
        self.is_database_device = True

    def save_event(self, event: Event) -> bool:
        try:
            logging.info(f'[SAVE EVENT] {event.get_type()}')
            save_entity(event, self.session)
            self.session.commit()
            logging.info(f'Event {event.get_type()} saved to database.')
            return True
        except Exception as e:
            logging.error(f'Error saving event to database: {e}')
            self.session.rollback()
            return False

    def process_message(self, event: Event) -> None:
        if event.get_type() in [EventType.ATTEMPT, EventType.DIAGNOSTIC]:
            try:
                self.save_event(event)
            except:
                logging.error(f'Error saving event to database: {event}')

        if event.get_type() == EventType.ATTEMPT:
            trigger = event.get_trigger_value()
            game = event.game

            if not isinstance(game, Game):
                super().process_message(event)
                return

            handler = GameHandler(game, self.session)
            handler.evaluate_trigger(trigger)

        super().process_message(event)

    def listen(self):
        consumer = KafkaConsumer(
            self._topic,
            client_id=self.device_code,
            value_deserializer=DatabaseMessageDecoder(self.session).db_decode_message_event,
        )

        if consumer.bootstrap_connected():
            print('Connected to Kafka.')

        for message in consumer:
            self.process_message(message.value)


class DatabaseMessageDecoder:
    def __init__(self, session: Session):
        self.session = session

    def db_decode_message_event(self, message: bytes) -> Event:
        data: dict = json.loads(message.decode('utf-8'))

        game_key = ('game_key' in data['event_data'].keys() and data['event_data']['game_key'] is not None)
        game = ('game' in data.keys() and data['game'] is not None)

        if game or game_key:
            if game_key:
                game_key = data['event_data']['game_key']
                game = retrieve_entity(game_key, entity_class=Game, session=self.session)
            else:
                game = data['game']

            return GameEvent(
                event_id=uuid.UUID(data['event_id']),
                event_type=EventType(data['event_type']),
                published=True,
                event_data=data['event_data'],
                game=game
            )

        return Event(
            event_id=uuid.UUID(data['event_id']),
            event_type=EventType(data['event_type']),
            published=True,
            event_data=data['event_data'],
        )

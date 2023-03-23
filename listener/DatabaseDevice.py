import json
import logging
import uuid

from kafka import KafkaConsumer
from sqlalchemy.orm import Session

from game.Game import Game
from listener.Device import Device
from listener.Event import Event, EventType
from data.database import get_connection, get_engine, save_entity, retrieve_entity


class DatabaseDevice(Device):
    def __init__(self, device_config: dict, device_code: str):
        super().__init__(device_config, device_code)
        self.session: Session = get_connection(engine=get_engine())
        self.is_database_device = True

    def process_message(self, event: Event) -> None:
        logging.info(f'[SAVE EVENT] {event.get_type()}')
        save_entity(event, self.session)
        self.session.commit()
        logging.info(f'Event {event.get_type()} saved to database.')

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

        game = None
        if 'game_key' in data['event_data'].keys():
            game_key = data['event_data']['game_key']
            game = retrieve_entity(game_key, entity_class=Game, session=self.session)

        return Event(
            event_id=uuid.UUID(data['event_id']),
            event_type=EventType(data['event_type']),
            published=True,
            event_data=data['event_data'],
            game=game
        )

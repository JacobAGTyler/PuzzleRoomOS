from typing import Optional

from kafka import KafkaConsumer

from listener.Interface import Interface
from listener.Event import Event, EventType, decode_message_event
from game.Game import Game


class Device:
    def __init__(self, device_config: dict, device_code: str):
        self.device_code = device_code
        self.device_config = device_config
        self._topic = device_config['topic']
        self._interfaces = []
        self._trigger_references: list[str] = []
        self.is_database_device = False

    def initialise(self, game: Optional[Game] = None):
        initialisation_event = Event(
            event_type=EventType.DEVICE_INITIALISATION,
            game=game,
            event_data={
                'device_code': self.device_code,
                'device_config': self.device_config,
                'device_interfaces': [interface.name for interface in self._interfaces]
            }
        )
        initialisation_event.publish()

    def add_interface(self, interface: Interface):
        print(interface.get_trigger_references())
        self._trigger_references += interface.get_trigger_references()
        self._interfaces.append(interface)

    def process_message(self, event: Event) -> None:
        if event.get_type() == EventType.GAME_END:
            for interface in self._interfaces:
                interface.deactivate()
                return

        if event.get_type() == EventType.GAME_START:
            trigger = event.get_trigger_value()

            if trigger is None:
                return

            if trigger in self._trigger_references:
                interface: Interface
                for interface in self._interfaces:
                    if interface.is_trigger(trigger):
                        interface.activate()

    def listen(self):
        consumer = KafkaConsumer(
            self._topic,
            client_id=self.device_code,
            value_deserializer=decode_message_event
        )

        if consumer.bootstrap_connected():
            print('Connected to Kafka.')

        for message in consumer:
            self.process_message(message.value)

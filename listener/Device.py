from typing import Optional

from kafka import KafkaConsumer

from listener.Interface import Interface
from listener.Event import Event, EventType
from utilities.config import import_config, ConfigType
from game.Game import Game


class Device:
    def __init__(self, device_config: dict):
        self.device_code = device_config['device_code']
        self.device_config = device_config
        self._topic = device_config['topic']
        self._interfaces = []

    def initialise(self, game: Optional[Game] = None):
        initialisation_event = Event(event_type=EventType.DEVICE_INITIALISATION, game=game, event_data={
            'device_code': self.device_code,
            'device_config': self.device_config,
            'device_interfaces': [interface.interface_code for interface in self._interfaces]
        })
        initialisation_event.publish()

        interface: Interface
        for interface in self._interfaces:
            interface.initialise()

    def add_interface(self, interface: Interface):
        self._interfaces.append(interface)

    def process_message(self, event: Event) -> None:
        pass

    def listen(self):
        consumer = KafkaConsumer('sample')

        if consumer.bootstrap_connected():
            good = True
            print('Connected to Kafka.')

        for message in consumer:
            print(message)


def instantiate_device(device_code):
    device_config = import_config(device_code, ConfigType.DEVICE)

    device = Device(device_config=device_config)

    for interface_config in device_config['interfaces']:
        interface = instantiate_interface(interface_config)
        device.add_interface(interface)

    return device
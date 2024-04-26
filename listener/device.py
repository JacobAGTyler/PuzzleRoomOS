from kafka import KafkaConsumer

from listener.Interface import Interface
from listener.event import Event, EventType, decode_message_event


class Device:
    def __init__(self, device_config: dict, device_code: str):
        self.device_code = device_code
        self.device_config = device_config
        self._broker_string = device_config['brokerConnectionString']
        self._topic = device_config['topic']
        self._interfaces = []
        self._trigger_references: list[str] = []
        self.is_database_device = False

    def initialise(self):
        print(f'Connecting to {self._broker_string}...')

        initialisation_event = Event(
            event_type=EventType.DEVICE_INITIALISATION,
            event_data={
                'device_code': self.device_code,
                'device_config': self.device_config,
                'device_interfaces': [interface.name for interface in self._interfaces]
            }
        )
        initialisation_event.publish()

    def add_interface(self, interface: Interface):
        self._trigger_references += interface.get_trigger_references()
        self._interfaces.append(interface)

    def process_message(self, event: Event) -> bool:
        if event.get_type() == EventType.GAME_END:
            for interface in self._interfaces:
                interface.deactivate()
                return True

        if event.get_type() == EventType.PUZZLE_SOLVE:
            trigger = event.get_trigger_value()

            if trigger is None:
                return False

            if trigger in self._trigger_references:
                interface: Interface
                for interface in self._interfaces:
                    if interface.is_trigger(trigger):
                        interface.activate()

    def listen(self):
        print(f'Connecting to `{self._broker_string}`...')

        consumer = KafkaConsumer(
            self._topic,
            client_id=self.device_code,
            value_deserializer=decode_message_event,
            bootstrap_servers=self._broker_string
        )

        if consumer.bootstrap_connected():
            print(f'Listening to topic {self._topic} on {self._broker_string}.')

        for message in consumer:
            self.process_message(message.value)

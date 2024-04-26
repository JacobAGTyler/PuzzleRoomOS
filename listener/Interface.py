import gpiozero as g

from listener.event import Event, EventType


def make_pin(pin_number: int, activate_high: bool) -> g.OutputDevice:
    gpio_string = f'GPIO{pin_number}'
    pin = g.OutputDevice(
        gpio_string,
        active_high=False,
        initial_value=False
    )
    return pin


class Interface:
    def __init__(self, trigger_references: list[str], config: dict):
        self.name = config['name']
        self._trigger_references = trigger_references

        pin = int(config['pin_number'])
        activate_high = bool(config['relay_on_activate'])

        self._relay_number = int(config['relay'])
        self._device = make_pin(pin_number=pin, activate_high=activate_high)

    def get_relay_number(self) -> int:
        return self._relay_number

    def get_trigger_references(self) -> list[str]:
        return self._trigger_references

    def is_trigger(self, trigger_reference: str) -> bool:
        return trigger_reference in self._trigger_references

    def activate(self):
        self._device.on()

    def deactivate(self):
        self._device.off()

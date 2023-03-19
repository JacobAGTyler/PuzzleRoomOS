import gpiozero as g
# import pigpio as p
import lgpio as lg

from gpiozero.pins.lgpio import LGPIOFactory


class Interface:
    def __init__(self, trigger_references: list[str]):
        self.interface_code = None
        self._trigger_references = trigger_references
        self.actions = []


factory = LGPIOFactory()

for i in range(26):
    dev = g.OutputDevice(i, initial_value=True, pin_factory=factory)
    dev.on()

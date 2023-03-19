import gpiozero as g

from gpiozero.pins.lgpio import LGPIOFactory


class Interface:
    def __init__(self, trigger_references: list[str]):
        self.interface_code = None
        self._trigger_references = trigger_references
        self.actions = []


factory = LGPIOFactory(chip=0)

for i in range(26):
    dev = g.OutputDevice(i, initial_value=True, pin_factory=factory)
    dev.on()

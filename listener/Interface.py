import gpiozero as g
# import pigpio as p

from gpiozero.pins.lgpio import LGPIOFactory


class Interface:
    def __init__(self, trigger_references: list[str]):
        self.interface_code = None
        self._trigger_references = trigger_references
        self.actions = []


factory = LGPIOFactory()

for i in range(28):
    g.OutputDevice(i, active_high=True, initial_value=False, pin_factory=factory)

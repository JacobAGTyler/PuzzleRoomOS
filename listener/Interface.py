import gpiozero as g
# import pigpio as p
import lgpio as lg

from gpiozero.pins.pigpio import PiGPIOFactory

lg.BOTH_EDGE = True


class Interface:
    def __init__(self, trigger_references: list[str]):
        self.interface_code = None
        self._trigger_references = trigger_references
        self.actions = []


factory = PiGPIOFactory(host='localhost')

for i in range(26):
    dev = g.OutputDevice(i, initial_value=True, pin_factory=factory)
    dev.on()

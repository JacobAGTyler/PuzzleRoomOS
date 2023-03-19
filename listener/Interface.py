import gpiozero as g

# from gpiozero.pins.native import NativeFactory
from gpiozero.pins.local import LocalPiFactory


class Interface:
    def __init__(self, trigger_references: list[str]):
        self.interface_code = None
        self._trigger_references = trigger_references
        self.actions = []


# factory = NativeFactory()
factory = LocalPiFactory().pin_class(g.OutputDevice)

for i in range(26):
    dev = g.OutputDevice(i, initial_value=True, pin_factory=factory)
    dev.on()

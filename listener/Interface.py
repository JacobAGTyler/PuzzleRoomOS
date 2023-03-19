import gpiozero as g


class Interface:
    def __init__(self, trigger_references: list[str]):
        self.interface_code = None
        self._trigger_references = trigger_references
        self.actions = []


for i in range(28):
    dev = g.OutputDevice(i, active_high=True, initial_value=False)
    dev.on()


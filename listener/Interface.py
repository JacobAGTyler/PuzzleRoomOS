import gpiozero as g

# from gpiozero.pins.native import NativeFactory


class Interface:
    def __init__(self, trigger_references: list[str]):
        self.interface_code = None
        self._trigger_references = trigger_references
        self.actions = []


# factory = NativeFactory()

for i in [18, 23, 24, 25, 12, 16, 20, 21]:
    gpio_pin = f'GPIO{i}'
    dev = g.OutputDevice(gpio_pin, initial_value=True)
    dev.on()

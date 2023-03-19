import gpiozero as g
import pigpio as p


class Interface:
    def __init__(self, trigger_references: list[str]):
        self.interface_code = None
        self._trigger_references = trigger_references
        self.actions = []


device1 = p.pi(host='192.168.0.164')

for i in range(28):
    device1.write(i, 1)

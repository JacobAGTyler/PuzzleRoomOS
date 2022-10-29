from listener.Interface import Interface


class Device:
    def __init__(self, device_config: dict):
        self.device_config = device_config
        self._interfaces = []

    def add_interface(self, interface: Interface):
        self._interfaces.append(interface)

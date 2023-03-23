import socket
from utilities.config import import_config, ConfigType

from listener.Device import Device
from listener.DatabaseDevice import DatabaseDevice
from listener.Interface import Interface


def instantiate_device(device_code: str = None):
    if device_code is None:
        device_code = socket.gethostname()
        device_code = device_code.split('.')[0]
        device_code = device_code.replace('puzzle-', '')

    device_config = import_config(device_code, ConfigType.DEVICE)
    db_device = device_config['isDatabase']

    if db_device:
        device = DatabaseDevice(device_config=device_config, device_code=device_code)
    else:
        device = Device(device_config=device_config, device_code=device_code)

    for interface_config in device_config['interfaces']:
        interface = Interface(
            trigger_references=[],
            config=interface_config
        )
        device.add_interface(interface)

    return device

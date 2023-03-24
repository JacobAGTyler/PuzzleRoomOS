import time
from kafka.errors import NoBrokersAvailable

from listener.Device import Device
from listener.device_factory import instantiate_device

timeout = 0
wait = 1


def increase_wait():
    global wait
    global timeout

    timeout += wait

    if timeout >= 10:
        wait = 10

    if timeout >= 60:
        wait = 60

    if timeout > 300:
        return False

    print(f'No brokers available, retrying in {wait} second(s). Timeout: {timeout}.')
    time.sleep(wait)

    return True


device: Device = instantiate_device()

do_loop = True
while do_loop:
    try:
        device.initialise()
        do_loop = False
    except NoBrokersAvailable as e:
        if not increase_wait():
            do_loop = False

do_loop = True
while do_loop:
    try:
        device.listen()
    except NoBrokersAvailable as e:
        if not increase_wait():
            do_loop = False


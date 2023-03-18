import time
from kafka.errors import NoBrokersAvailable

from listener.Device import Device, instantiate_device

do_loop = True
timeout = 0
wait = 1

good = False

while do_loop:
    try:
        device_code_input = input('Enter Device Code:')

        if device_code_input == 'exit':
            do_loop = False
            continue

        device = instantiate_device(device_code=device_code_input)

        device.listen()
    except NoBrokersAvailable as e:
        timeout += wait

        if timeout >= 10:
            wait = 10

        if timeout >= 60:
            wait = 60

        if timeout > 300:
            do_loop = False

        print(f'No brokers available, retrying in {wait} second(s). Timeout: {timeout}.')
        time.sleep(wait)

import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

do_loop = True

while do_loop:
    try:
        consumer = KafkaConsumer('sample')
        for message in consumer:
            print(message)
    except NoBrokersAvailable as e:
        time.sleep(1)

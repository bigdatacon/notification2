import time
import json
from uuid import uuid4
from confluent_kafka import Producer

jsonString1 = """ {"name":"Gal", "email":"Gadot84@gmail.com", "salary": "8345.55"} """
jsonString2 = """ {"name":"Dwayne", "email":"Johnson52@gmail.com", "salary": "7345.75"} """
jsonString3 = """ {"name":"Momoa", "email":"Jason91@gmail.com", "salary": "3345.25"} """

from confluent_kafka import Producer

p = Producer({"bootstrap.servers": "localhost:9092"})

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

# for data in some_data_source:
    # Trigger any available delivery report callbacks from previous produce() calls
p.poll(0)

# Asynchronously produce a message, the delivery report callback
# will be triggered from poll() above, or flush() below, when the message has
# been successfully delivered or failed permanently.
p.produce('example_topic', jsonString1.encode('utf-8'), callback=delivery_report)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
p.flush()
print(f'все доставлено')
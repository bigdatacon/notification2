import time
import json
from uuid import uuid4
from confluent_kafka import Producer

jsonString1 = """ {"name":"Gal", "email":"Gadot84@gmail.com", "salary": "8345.55"} """
jsonString2 = """ {"name":"Dwayne", "email":"Johnson52@gmail.com", "salary": "7345.75"} """
jsonString3 = """ {"name":"Momoa", "email":"Jason91@gmail.com", "salary": "3345.25"} """
# print(type(jsonString3))

from confluent_kafka import Producer

class KafkaProducersender:
    def __init__(self):
        self.p = Producer({"bootstrap.servers": "localhost:9092"})

    def delivery_report(self,err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def send(self,topic_name, data):
        self.p.poll(0)
        # topic_name = 'example_topic'

        # Asynchronously produce a message, the delivery report callback
        # will be triggered from poll() above, or flush() below, when the message has
        # been successfully delivered or failed permanently.

        self.p.produce(topic_name, data.encode('utf-8'), callback=self.delivery_report)



        # Wait for any outstanding messages to be delivered and delivery report
        # callbacks to be triggered.
        self.p.flush()
        print(f'все доставлено')

if __name__ == '__main__':
    p = KafkaProducersender()
    topic_name = 'example_topic'
    data = """ {"name":"Dwayne", "email":"Johnson58@gmail.com", "salary": "778345.75"} """
    p.send(topic_name, data)
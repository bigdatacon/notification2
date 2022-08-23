from confluent_kafka import Consumer
from time import sleep
# c.subscribe(['example_topic'])

class KafkaConsumerMy(Consumer):
    def __init__(self, topic):
        self.consumer =  Consumer({
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'mygroup',
            'auto.offset.reset': 'earliest'
        })

        self.consumer.subscribe(topic)

    def subscribe(self):
        print(f' eto self.consumer : {self.consumer}')
        return self.consumer




# RUNNING CONSUMER FOR READING MESSAGE FROM THE KAFKA TOPIC
consumer = KafkaConsumerMy(['example_topic']).subscribe()
try:
    while True:
        print("Listening")
        # read single message at a time
        msg = consumer.poll(0)

        if msg is None:
            sleep(5)
            continue
        if msg.error():
            print("Error reading message : {}".format(msg.error()))
            continue
        # You can parse message and save to data base here
        print(msg)
        consumer.commit()

except Exception as ex:
    print("Kafka Exception : {}", ex)

finally:
    print("closing consumer")
    consumer.close()
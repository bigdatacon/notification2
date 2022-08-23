from confluent_kafka import Consumer
from time import sleep
# c.subscribe(['example_topic'])

class KafkaConsumerMy:
    def __init__(self, topic: str):
        self.consumer =  Consumer({
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'mygroup',
            'auto.offset.reset': 'earliest'
        })

        self.consumer.subscribe(['example_topic'])
        print(f' eto self.consumer = {self.consumer}')

    def start_listener(self):
        try:
            while True:
                print("Listening")
                # read single message at a time
                msg = self.consumer.poll(0)

                if msg is None:
                    sleep(5)
                    continue
                if msg.error():
                    print("Error reading message : {}".format(msg.error()))
                    continue
                # You can parse message and save to data base here
                print(msg)
                self.consumer.commit()
        except Exception as ex:
            print("Kafka Exception : {}", ex)

        finally:
            print("closing consumer")
            self.consumer.close()


# RUNNING CONSUMER FOR READING MESSAGE FROM THE KAFKA TOPIC
my_consumer = KafkaConsumerMy('example_topic')
my_consumer.start_listener()
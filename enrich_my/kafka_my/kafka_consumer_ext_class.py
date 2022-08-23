from confluent_kafka import Consumer
from time import sleep

class ExampleConsumer:
    broker = "localhost:9092"
    topic = "example_topic"
    group_id = "mygroup"

    def start_listener(self):
        consumer_config = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'mygroup',
            'auto.offset.reset': 'earliest'
        }

        consumer = Consumer(consumer_config)
        consumer.subscribe([self.topic])

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

#RUNNING CONSUMER FOR READING MESSAGE FROM THE KAFKA TOPIC
my_consumer = ExampleConsumer()
my_consumer.start_listener()
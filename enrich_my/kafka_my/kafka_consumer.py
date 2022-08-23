from kafka import KafkaConsumer


class KafkaConsumerMy:
    def __init__(self,topic, host, port):
        self.topic = topic
        self.host = host
        self.port = port
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=[f'{self.host}:{self.port}'],
            auto_offset_reset='earliest',
            group_id='echo-messages-to-stdout',
        )
    def read(self):
        for message in self.consumer:
            return message.value

# consumer = KafkaConsumer(
#     'example_topic',
#     bootstrap_servers=['localhost:9092'],
#     auto_offset_reset='earliest',
#     group_id='echo-messages-to-stdout',
# )

# for message in consumer:
#     print(message.value)

if __name__ == '__main__':
    consumer = KafkaConsumerMy('example_topic', 'localhost', '9092')
    while True:
        print(consumer.read())
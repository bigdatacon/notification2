from kafka import KafkaConsumer


class KafkaConsumerMy_prot:
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
        self.messages = []
    def read(self):
        for message in self.consumer:
            yield message.value



# consumer = KafkaConsumer(
#     'example_topic',
#     bootstrap_servers=['localhost:9092'],
#     auto_offset_reset='earliest',
#     group_id='echo-messages-to-stdout',
# )

# for message in consumer:
#     print(message.value)

if __name__ == '__main__':
    consumer = KafkaConsumerMy_prot('example_topic', 'localhost', '9092')
    while True:
        res = consumer.read()
        for i in res:
            print(f' eto i : {i}')
        # print(consumer.read_once())

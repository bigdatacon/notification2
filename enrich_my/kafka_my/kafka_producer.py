from kafka import KafkaProducer
from time import sleep


producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

producer.send(
    topic='example_topic',
    value=b'1611039981',
    key=b'500281+tt0120338',
)

sleep(1)
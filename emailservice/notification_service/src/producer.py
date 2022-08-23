"""Kafka producer."""

import logging

from confluent_kafka import Producer

# Initialize logger
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


class KafkaProducer:
    """Kafka Producer."""

    def __init__(self, config):
        """Initialization.

        :param config:
        """
        self.config = config
        self.producer = Producer(self.config)

    def delivery_report(self, err, msg):
        """Called once for each message produced to indicate delivery result.

        :param err: Ошибка.
        :param msg: Сообщение.
        :return: None
        """
        if err is not None:
            logging.info('Message delivery failed: {}'.format(err))
        else:
            logging.info('Message delivered to {} [{}]'.format(
                msg.topic(), msg.partition()
            ))

    def produce(self, topic, msg):
        """Produce.

        :param topic:
        :param msg:
        :return:
        """
        logging.info('Send message synchronously')
        self.producer.produce(
            topic,
            msg,
            callback=lambda err, original_msg=msg: self.delivery_report(
                err, original_msg
            ),
        )
        self.producer.flush()

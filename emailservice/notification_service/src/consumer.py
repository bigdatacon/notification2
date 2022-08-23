"""Consumer."""

import logging
import sys

from confluent_kafka import Consumer, KafkaError, KafkaException

# Initialize logger
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


class KafkaConsumer:
    """KafkaConsumer."""

    def __init__(
            self,
            config,
            kafka_min_commit_count=1,
            max_bulk_messages=10,
            max_timeout=5,
    ):
        """Initialization.

        :param config:
        :param kafka_min_commit_count:
        :param max_bulk_messages:
        :param max_timeout:
        """
        self.config = config
        self.kafka_min_commit_count = kafka_min_commit_count
        self.max_bulk_messages = max_bulk_messages
        self.max_timeout = max_timeout

        self.consumer = Consumer(self.config)
        self.running = True

    def subscribe(self, topics):
        """Subscribe.

        :param topics:
        :return:
        """
        self.consumer.subscribe(topics)

    def raise_on_error(self, msg):
        """Raise on error.

        :raise KafkaException:
        :param msg:
        :return:
        """
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                sys.stderr.write('%% %s [%d] reached end at offset %d\n' % (
                    msg.topic(),
                    msg.partition(),
                    msg.offset()
                ))
            elif msg.error():
                raise KafkaException(msg.error())
            return True
        return False

    def consume_loop(self, msg_process):
        """Consume loop.

        :param msg_process: msg_process.
        :return: None.
        """
        msg_bulk = []
        msg_count = 0
        while self.running:
            msg = self.consumer.poll(timeout=self.max_timeout)
            if msg is None or self.raise_on_error(msg):
                continue

            logging.info(f'Received message from topic "{msg.topic()}"')

            msg_count += 1
            msg_bulk.append(msg)

            if len(msg_bulk) >= self.max_bulk_messages:
                msg_process(msg_bulk)
                msg_bulk = []
                if msg_count % self.kafka_min_commit_count == 0:
                    self.consumer.commit(asynchronous=False)

    def run(self, topics, msg_process):
        """Run.

        :param topics:
        :param msg_process:
        :return:
        """
        try:
            self.subscribe(topics)

            self.consume_loop(msg_process)
        except BaseException:
            pass
        finally:
            # Close down consumer to commit final offsets.
            self.consumer.close()

    def shutdown(self):
        """Shutdown.

        :return:
        """
        self.running = False

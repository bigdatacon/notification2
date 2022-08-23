"""Kafka create topics."""

import json
import logging

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError


class Kafka:
    """Kafka."""

    def __init__(self, servers_name=None, client_id='default_user'):
        """Initialization.

        :param servers_name:
        :param client_id:
        """
        if servers_name is None:
            servers_name = ['kafka:29092', ]

        self.admin_client = KafkaAdminClient(bootstrap_servers=servers_name, client_id=client_id)

    def create_topic(self, topic_name=None, num_partitions=1, replication_factor=1):
        """Create topic.

        :param topic_name:
        :param num_partitions:
        :param replication_factor:
        :return:
        """
        try:
            self.admin_client.create_topics(
                new_topics=[NewTopic(
                    name=topic_name,
                    num_partitions=num_partitions,
                    replication_factor=replication_factor
                )],
                validate_only=False
            )
            logging.info(f'Topic "{topic_name}" successfully created!')
        except TopicAlreadyExistsError:
            logging.info(f'Topic "{topic_name}" is already exist.')


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    with open('./scripts/topics.json') as json_file:
        topics = json.load(json_file)

    kafka = Kafka(client_id='user_initialize_topics')
    for topic in topics:
        kafka.create_topic(topic_name=topic['name'])

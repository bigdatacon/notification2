"""Main."""

import json
import logging
from typing import List

import config
from consumer import KafkaConsumer
from producer import KafkaProducer

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


def craft_notification_message(
        template_name: str,
        user_ids: List[str],
        queue: str
) -> dict:
    """Craft notification message.

    :param template_name:
    :param user_ids:
    :param queue:
    :return:
    """
    return {
        'template_name': template_name,
        'user_ids': user_ids,
        'queue': queue
    }


def topic_likes_data(data):
    """Topic likes data.

    :param data:
    :return:
    """
    return craft_notification_message(
        config.USER_REGISTRATION_TEMPLATE,
        [
            d.get(config.USER_ID_FIELD)
            for d in data
        ],
        config.STANDART_QUEUE
    )


def load(data, consumer_topic_name, producer_topic_name=config.NOTIFICATIONS_TOPIC_NAME):
    """Load.

    :param data:
    :param consumer_topic_name:
    :param producer_topic_name:
    :return:
    """
    message = None

    if consumer_topic_name == 'likes':
        message = topic_likes_data(data)

    if message:
        producer.produce(
            producer_topic_name,
            json.dumps(message)
        )
        data_len = len(data)
        logging.info(f"Loaded {data_len} rows in '{producer_topic_name}'")
    else:
        logging.info(f"Nothing to load in '{producer_topic_name}'")


def transform(messages):
    """Transform.

    :param messages:
    :return:
    """
    topics_data = {}
    for msg in messages:
        topics_data.setdefault(msg.topic(), [])
        topics_data[msg.topic()].append(json.loads(msg.value().decode('utf-8')))

    for name, data in topics_data.items():
        load(data, name)


if __name__ == '__main__':
    producer = KafkaProducer(
        config=config.KAFKA_PRODUCER_CONFIG
    )

    consumer = KafkaConsumer(
        config=config.KAFKA_CONSUMER_CONFIG,
        kafka_min_commit_count=config.KAFKA_MIN_COMMIT_COUNT,
        max_bulk_messages=config.KAFKA_MAX_BULK_MESSAGES,
        max_timeout=config.KAFKA_MAX_CONSUMER_TIMEOUT,
    )
    consumer.run(topics=config.KAFKA_CONSUMER_TOPICS, msg_process=transform)

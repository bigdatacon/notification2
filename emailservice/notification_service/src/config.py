"""Configurations of notification service."""

import os

USER_REGISTRATION_TEMPLATE = 'user_registered'
USER_ID_FIELD = 'user_id'
STANDART_QUEUE = 'standart'

REGISTRATION_TOPIC_NAME = 'registration'
NOTIFICATIONS_TOPIC_NAME = 'notifications'

kafka_host = os.getenv('KAFKA_HOST', 'kafka')
kafka_port = os.getenv('KAFKA_PORT', '29092')

KAFKA_PRODUCER_CONFIG = {
    'bootstrap.servers': f'{kafka_host}:{kafka_port}',
    'socket.timeout.ms': int(os.getenv('KAFKA_MAX_PRODUCER_TIMEOUT', 100)),
    'api.version.request': 'false',
    'broker.version.fallback': '0.9.0',
}

KAFKA_CONSUMER_CONFIG = {
    'bootstrap.servers': f'{kafka_host}:{kafka_port}',
    'group.id': 'etl_process',
    'enable.auto.commit': False,
    'auto.offset.reset': 'earliest'
}

KAFKA_MIN_COMMIT_COUNT = int(os.getenv('KAFKA_MIN_COMMIT_COUNT', 1))
KAFKA_MAX_BULK_MESSAGES = int(os.getenv('KAFKA_MAX_BULK_MESSAGES', 10))
KAFKA_MAX_CONSUMER_TIMEOUT = int(os.getenv('KAFKA_MAX_CONSUMER_TIMEOUT', 5))

KAFKA_CONSUMER_TOPICS = [REGISTRATION_TOPIC_NAME]

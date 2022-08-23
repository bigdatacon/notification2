"""Worker config."""

import os

EMAIL_SHIPPING_METHOD = 'email'

NOTIFICATIONS_TOPIC_NAME = 'notifications'

kafka_host = os.getenv('KAFKA_HOST', 'kafka')
kafka_port = os.getenv('KAFKA_PORT', '29092')

# Kafka consumer
KAFKA_CONSUMER_CONFIG = {
    'bootstrap.servers': f'{kafka_host}:{kafka_port}',
    'group.id': 'etl_process',
    'enable.auto.commit': False,
    'auto.offset.reset': 'earliest'
}
KAFKA_MIN_COMMIT_COUNT = int(os.getenv('KAFKA_MIN_COMMIT_COUNT', 1))
KAFKA_MAX_BULK_MESSAGES = int(os.getenv('KAFKA_MAX_BULK_MESSAGES', 10))
KAFKA_MAX_CONSUMER_TIMEOUT = int(os.getenv('KAFKA_MAX_CONSUMER_TIMEOUT', 5))
# Topics to check
KAFKA_CONSUMER_TOPICS = [NOTIFICATIONS_TOPIC_NAME]

SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = os.getenv('SMTP_PORT', 465)
SMTP_USER = os.getenv('SMTP_USER', 'example@gmail.com')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'password')  # https://support.google.com/accounts/answer/185833

SUBJECT = 'Hello from super movie portal!'

ENRICHMENT_SERVICE_URL = os.getenv('ENRICHMENT_SERVICE_URL', 'http://enrichment_service/api/v1/message')

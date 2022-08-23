"""Main."""

import json

import backoff as backoff
import config
import requests
from consumer import KafkaConsumer
from senders.EmailSender import EmailSender

senders: list = []


def load(messages):
    """Load.

    :param messages:
    [{
        "shipping_methods": ["email"],
        "user_data": {
            "312e17cc-835c-4171-ab33-eb2690051b8b": {
                "email": "example@mail.com",
                ...
            }
        },
        "message_bodies": {
            "312e17cc-835c-4171-ab33-eb2690051b8b": "тело письма"
        }
    }]
    """
    for sender in senders:
        sender.send_many([msg for msg in messages if sender.match_shipment_method(msg['shipping_methods'])])


def craft_template(template: str, data: dict) -> str:
    """Craft template.

    :param template:
    :param data:
    :return:
    """
    # FIXME очень неоптимально!
    result = template
    for key, value in data.items():
        result.replace(f'{{{{{key}}}}}', value)
    return result


@backoff.on_exception(backoff.expo,
                      (requests.exceptions.ConnectionError, requests.exceptions.HTTPError)
                      )
def enrich_message(message):
    """Enrich message.

    :param message:
    :return:
    """
    response = requests.post(
        config.ENRICHMENT_SERVICE_URL,
        json=json.loads(message)
    )
    response.raise_for_status()
    return response.json()


def transform(messages):
    """Transform.

    :param messages:
    :return:
    """
    enriched_msgs = []
    for msg in messages:
        decoded_msg = msg.value().decode('utf-8')
        enriched_msgs.append(enrich_message(decoded_msg))

    for msg in enriched_msgs:
        message_bodies = {}
        for user_id, data in msg['user_data'].items():
            message_bodies[user_id] = craft_template(
                template=msg['template'],
                data=data
            )
        msg['message_bodies'] = message_bodies

    load(enriched_msgs)


if __name__ == '__main__':
    senders.append(
        EmailSender()
    )

    consumer = KafkaConsumer(
        config=config.KAFKA_CONSUMER_CONFIG,
        kafka_min_commit_count=config.KAFKA_MIN_COMMIT_COUNT,
        max_bulk_messages=config.KAFKA_MAX_BULK_MESSAGES,
        max_timeout=config.KAFKA_MAX_CONSUMER_TIMEOUT,
    )
    consumer.run(topics=config.KAFKA_CONSUMER_TOPICS, msg_process=transform)

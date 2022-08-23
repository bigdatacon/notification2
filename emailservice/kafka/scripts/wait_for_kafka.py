"""Wait for kafka."""

import logging
import time

from kafka import KafkaAdminClient
from kafka.errors import NoBrokersAvailable


def main():
    """Main."""
    servers_name = ['kafka:29092', ]
    logging.info('Connecting to Kafka...')
    while True:
        try:
            client = KafkaAdminClient(
                bootstrap_servers=servers_name,
                client_id='default_user'
            )
            if client:
                logging.info('Connected')
                exit()
        except NoBrokersAvailable:
            logging.info("Can't connect to Kafka on host %s", servers_name)
            time.sleep(3)


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    main()

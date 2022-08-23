"""Wait for postgres."""

import logging
import os
import time

import psycopg2


def main():
    """Main."""
    dsl = {'dbname': os.environ.get('pg_dbname', 'notifications'),
           'user': os.environ.get('pg_username', 'postgres'),
           'password': os.environ.get('pg_password', 'mysecretpassword'),
           'host': os.environ.get('pg_hosthame', 'postgres'),
           'port': os.environ.get('pg_port', 5432),
           'options': os.environ.get('pg_options', '-c search_path=content,public'),
           }
    while True:
        try:
            psycopg2.connect(**dsl)
        except (OSError, psycopg2.OperationalError) as e:
            logging.info(e)
            time.sleep(3)
        else:
            logging.info('Postgres connected')
            exit()


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logging.info('Waiting for Postgres ...')
    main()

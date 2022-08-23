
"""Wait for postgres."""

import logging
import os
import time
from services.authmy import AuthServiceMy

import psycopg2


class PGConnection:
    """Класс описывающий подключение к PG на вход название database из PG."""
    def __init__(
            self,
            dbname: str
    ):
        self.dbname = dbname

    def main(self):
        """Main."""
        dsl = {'dbname': self.dbname,
               # 'dbname': os.environ.get('pg_dbname', 'auth'),
               'user': os.environ.get('pg_username', 'postgres'),
               'password': os.environ.get('pg_password', 'password'),
               # 'host': os.environ.get('pg_hosthame', 'postgres'),
               'host': os.environ.get('pg_hosthame', 'localhost'),
               'port': os.environ.get('pg_port', 5432),
               'options': os.environ.get('pg_options', '-c search_path=content,public'),
               }
        while True:
            try:
                psycopg2.connect(**dsl)
                connection = psycopg2.connect(**dsl)
            except (OSError, psycopg2.OperationalError) as e:
                logging.info(e)
                time.sleep(3)
            else:
                logging.info('Postgres connected')
                return connection
                exit()


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    logging.info('Waiting for Postgres ...')
    connection = PGConnection('auth').main()
    print(f' eto connection : {connection}')
    cursor = connection.cursor()
    cursor.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")
    print(cursor.fetchall())
    id_seek = 'a61846cf-8882-4213-a471-f763000d1147'
    postgreSQL_select_Query = "select * from public.user ;"
    cursor.execute(postgreSQL_select_Query)
    print(cursor.fetchall())

    cursor.execute("select username, first_name, last_name from public.user  WHERE id = (%s);", (id_seek,))
    print("Selecting rows from mobile table using cursor.fetchall")
    print(cursor.fetchall())
    print(f' eto AuthServiceMy : {AuthServiceMy(connection).get_by_id(id_seek)}')

    cursor.execute("select id username, first_name, last_name from public.user ;")
    print("Selecting all ids rows from mobile table using cursor.fetchall")
    print(cursor.fetchall())
    print(f' eto AuthServiceMy get all : {AuthServiceMy(connection).get_all_users_info_from_table()}')

    # print(f' eto AuthService : {AuthService(connection).get_by_id(id_seek)}')  ## Не работает вызов функции в email/enrich_my/wait_for_pg.py



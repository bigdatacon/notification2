"""Cron service Data base."""

import psycopg2
from psycopg2.extras import DictCursor


class DatabaseConnector:
    """Database Connector."""

    def __init__(self, **dsl):
        """Initialization."""
        self.conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)

    def get_rows(self, sql, args: list = None):
        """Get rows.

        :param sql:
        :param args:
        :return:
        """
        with self.conn.cursor() as cursor:
            prepped_sql = cursor.mogrify(sql, args)
            cursor.execute(prepped_sql)
            return cursor.fetchall()

"""Configuration of cron service."""

import logging

from pydantic import BaseSettings, Field, ValidationError


class Config(BaseSettings):
    """Config."""

    class Config:
        """Config."""

        env_file = None

    pg_hostname: str = Field(env='pg_hosthame', default='postgres')
    pg_port: int = Field(env='pg_port', default=5432)
    pg_dbname: str = Field(env='pg_dbname', default='notifications')
    pg_user: str = Field(env='pg_username', default='postgres')
    pg_password: str = Field(env='pg_password', default='mysecretpassword')
    pg_options: str = Field(
        env='pg_options',
        default='-c search_path=content,public'
    )

    manager_period: int = Field(env='manager_period', default=15)
    standart_queue = 'standart'

    kafka_host: str = Field(env='kafka_host', default='kafka')
    kafka_port: str = Field(env='kafka_port', default='29092')
    kafka_max_producer_timeout: int = Field(env='kafka_max_producer_timeout', default=100)

    kafka_producer_topic_name: str = Field(env='kafka_producer_topic_name', default='notifications')


try:
    config = Config(_env_file=None)
except ValidationError:
    logging.error(ValidationError)

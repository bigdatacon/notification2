"""Cron service Main."""

import json
import logging
import re
import time
from datetime import date
from typing import Dict, List, Optional, Set, Tuple

import regex
import schedule
from config import config
from db import DatabaseConnector
from models import ScheduledNotification
from producer import KafkaProducer

# Initialize logger
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

schedule_every_week = {
    '1': schedule.every().monday,
    '2': schedule.every().tuesday,
    '3': schedule.every().wednesday,
    '4': schedule.every().thursday,
    '5': schedule.every().friday,
    '6': schedule.every().saturday,
    '7': schedule.every().sunday
}

running_notifications: Dict[str, ScheduledNotification] = {}


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


def get_scheduled_notification() -> List[ScheduledNotification]:
    """Get scheduled notification.

    :return:
    """
    sql = """SELECT sn.id, sn.schedule, t.template_name, sn.data, sn.last_update_time, sn.enabled
    FROM public.scheduled_notification sn
    LEFT JOIN template t on sn.template_id = t.id;"""

    return [
        ScheduledNotification(*n) for n in db_connector.get_rows(sql)
    ]


def get_user_ids(notification_id: str) -> list:
    """Get user ids.

    :param notification_id:
    :return:
    """
    sql = """SELECT user_id 
    FROM scheduled_notification_user 
    WHERE scheduled_notification_id = %s;"""

    return db_connector.get_rows(sql, [notification_id])


def job(notification: ScheduledNotification, month_day: Optional[str] = None):
    """Job.

    :param notification:
    :param month_day:
    :return:
    """
    if month_day and date.today().day != int(month_day):
        logging.info('{}:{} returned by day'.format(
            notification.id, notification.template_name
        ))
        return
    notification.user_ids = get_user_ids(notification.id)
    if len(notification.user_ids) == 0:
        logging.info('{}:{} returned by users len'.format(
            notification.id, notification.template_name
        ))
        return

    message = craft_notification_message(
        notification.template_name,
        notification.user_ids,
        config.standart_queue
    )
    producer.produce(
        config.kafka_producer_topic_name,
        json.dumps(message)
    )
    logging.info('Loaded {}:{} in {}'.format(
        notification.id, notification.template_name, config.kafka_producer_topic_name
    ))


def get_notifications_statuses(
        notifications_from_database: List[ScheduledNotification],
        running_notifications: Dict[str, ScheduledNotification]
) -> Tuple[Set[str], Set[str]]:
    """Get notifications statuses.

    :param notifications_from_database:
    :param running_notifications:
    :return:
    """
    notifications_to_disable_ids = set()
    notifications_to_enable_ids = set()

    for notification in notifications_from_database:
        running = running_notifications.get(notification.id)

        if notification.enabled:
            if not running:
                running_notifications[notification.id] = notification
                notifications_to_enable_ids.add(notification.id)
            elif running.last_update_time != notification.last_update_time:
                notifications_to_disable_ids.add(notification.id)
                running_notifications[notification.id] = notification
                notifications_to_enable_ids.add(notification.id)
        elif running:
            notifications_to_disable_ids.add(notification.id)
            del running_notifications[notification.id]

    for not_id in set(running_notifications.keys()) - set(n.id for n in notifications_from_database):
        notifications_to_disable_ids.add(not_id)

    return notifications_to_disable_ids, notifications_to_enable_ids


def disable_notifications(ids: Set[str]):
    """Disable notifications.

    :param ids:
    :return:
    """
    for user_id in ids:
        schedule.clear(user_id)


def start_monthly(notification: ScheduledNotification) -> bool:
    """Start monthly.

    :param notification:
    :return:
    """
    monthly_match = re.findall(regex.monthly_regex, notification.schedule)
    if monthly_match:
        schedule.every().day.at('{}:{}'.format(monthly_match[0][1], monthly_match[0][2])).do(
            job,
            notification=notification,
            month_day=monthly_match[0][0]
        ).tag(notification.id)
        return True
    return False


def start_weekly(notification: ScheduledNotification) -> bool:
    """Start weekly.

    :param notification:
    :return:
    """
    weekly_match = re.findall(regex.weekly_regex, notification.schedule)
    if weekly_match:
        schedule_every_week[weekly_match[0][0]].at('{}:{}'.format(weekly_match[0][1], weekly_match[0][2])).do(
            job,
            notification=notification,
        ).tag(notification.id)
        return True
    return False


def start_daily(notification: ScheduledNotification) -> bool:
    """Start daily.

    :param notification:
    :return:
    """
    daily_match = re.findall(regex.daily_regex, notification.schedule)
    if daily_match:
        schedule.every().day.at('{}:{}'.format(daily_match[0][0], daily_match[0][1])).do(
            job,
            notification=notification,
        ).tag(notification.id)
        return True
    return False


def enable_notifications(ids: Set[str]):
    """Enable notifications.

    :param ids:
    :return:
    """
    for user_id in ids:
        notification = running_notifications[user_id]

        logging.info('Starting {}:{} notification'.format(
            notification.id, notification.template_name
        ))

        result_notify = start_monthly(notification) or start_weekly(notification) or start_daily(notification)

        if not result_notify:
            logging.error('Notification {}:{} has invalid schedule format: {}'.format(
                notification.id, notification.template_name, notification.schedule
            ))
            del running_notifications[notification.id]


def manage_schedule():
    """Shedule."""
    scheduled_notifications = get_scheduled_notification()
    notifications_to_disable_ids, notifications_to_enable_ids = get_notifications_statuses(
        notifications_from_database=scheduled_notifications,
        running_notifications=running_notifications
    )
    disable_notifications(notifications_to_disable_ids)
    enable_notifications(notifications_to_enable_ids)


if __name__ == '__main__':
    producer = KafkaProducer(
        config={
            'bootstrap.servers': f'{config.kafka_host}:{config.kafka_port}',
            'socket.timeout.ms': config.kafka_max_producer_timeout,
            'api.version.request': 'false',
            'broker.version.fallback': '0.9.0',
        }
    )

    db_connector = DatabaseConnector(
        dbname=config.pg_dbname,
        user=config.pg_user,
        password=config.pg_password,
        host=config.pg_hostname,
        port=config.pg_port,
        options=config.pg_options,
    )
    manage_schedule()

    schedule.every(config.manager_period).minutes.do(manage_schedule)

    while True:
        schedule.run_pending()
        time.sleep(1)

"""Email Sender."""

import smtplib
from email.message import EmailMessage
from typing import List

import config
from senders.sender import AbstractSender


class EmailSender(AbstractSender):
    """Email Sender."""

    shipment_method = 'email'
    smtp_class = smtplib.SMTP_SSL if config.SMTP_PORT == 465 else smtplib.SMTP

    def match_shipment_method(self, methods: List[str]) -> bool:
        """Match shipment method.

        :param methods:
        :return: bool
        """
        return any([method == self.shipment_method for method in methods])

    def send_one(self, to, subject, content):
        """Send one.

        :param to:
        :param subject:
        :param content:
        :return: None
        """
        with self.smtp_class(config.SMTP_HOST, config.SMTP_PORT) as server:
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)

            message = EmailMessage()
            message['From'] = config.SMTP_USER
            message['To'] = ','.join([to])
            message['Subject'] = subject

            message.add_alternative(content, subtype='html')
            server.sendmail(config.SMTP_USER, [to], message.as_string())

    def send_many(self, messages):
        """Send many.

        :param messages: messages
        :return: None
        """
        for message in messages:
            for user_id, data in message['user_data'].items():
                self.send_one(
                    to=data['email'],
                    subject=config.SUBJECT,  # TODO забыл совсем про темы сообщения
                    content=message['message_bodies'][user_id]
                )

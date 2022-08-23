"""Enrichment service Notifications."""

from typing import Optional

from asyncpg import Pool
from core.config import logger
from db.notification import get_pool
from fastapi import Depends
from schemas.base import Template


class NotificationService:
    """Notification Service."""

    def __init__(self, db: Pool):
        """Initialization."""
        self.db = db

    async def get_notification_template(self, template_name) -> Optional[Template]:
        """Asunc get notification template.

        :param template_name:
        :return:
        """
        try:
            async with self.db.acquire() as con:
                row = await con.fetchrow(
                    'SELECT template_text, send_via_email, send_via_sms FROM public.template WHERE template_name=$1',
                    template_name
                )

                template = Template.parse_obj(dict(row))
                logger.info(f'Get template: {template}')

            return template

        except Exception:
            logger.exception('Can not found template id in notification database.')

        return None


# @lru_cache()
def get_notification_service(
        notification: Pool = Depends(get_pool),
) -> NotificationService:
    """Get notification service.

    :param notification:
    :return:
    """
    return NotificationService(db=notification)

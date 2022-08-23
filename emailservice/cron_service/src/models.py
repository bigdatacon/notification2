"""Models."""

import datetime
from typing import Optional

from pydantic import BaseModel


class ScheduledNotification(BaseModel):
    """Scheduled Notification."""

    id: str
    schedule: str
    template_name: str
    data: Optional[dict]
    last_update_time: datetime.datetime
    enabled: bool
    user_ids: Optional[str] = None

    def __init__(self, id, schedule, template_name, data, last_update_time, enabled):
        super().__init__(
            id=id,
            schedule=schedule,
            template_name=template_name,
            data=data,
            last_update_time=last_update_time,
            enabled=enabled
        )

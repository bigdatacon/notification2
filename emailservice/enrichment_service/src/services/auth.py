"""Auth."""

import uuid
from typing import List, Optional

from asyncpg import Pool
from core.config import logger
from db.auth import get_pool
from fastapi import Depends
from schemas.base import UserResponse


class AuthService:
    """AuthService."""

    def __init__(self, db: Pool):
        """Initialization.

        :param db:
        """
        self.db = db

    async def get_by_id(self, user_id: uuid.UUID) -> UserResponse:
        """Get user info by id.

        :param user_id:
        :return:
        """
        try:
            async with self.db.acquire() as con:
                row = await con.fetchrow(
                    'SELECT id, username, email FROM public.user WHERE id=$1', user_id
                )

                user = UserResponse.parse_obj(dict(row))
                logger.info(f'Get user: {user}')

            return user

        except Exception:
            logger.exception('Can not found user id in auth database.')

    async def get_many_by_ids(self, user_ids: List[uuid.UUID]) -> Optional[List[UserResponse]]:
        """Get many by ids.

        :param user_ids:
        :return:
        """
        try:
            async with self.db.acquire() as con:
                rows = await con.fetch(
                    'SELECT id, username, email FROM public.user WHERE id = any($1::uuid[])',
                    user_ids,
                )
            return [
                UserResponse.parse_obj(dict(row)) for row in rows
            ]

        except Exception:
            logger.exception('Can not found users in auth database.')

        return None


# @lru_cache()
def get_auth_service(
        auth: Pool = Depends(get_pool),
) -> AuthService:
    """Get auth service.

    :param auth:
    :return:
    """
    return AuthService(db=auth)

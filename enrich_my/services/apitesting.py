"""Auth."""
from functools import lru_cache
import uuid
from typing import List, Optional

from asyncpg import Pool
from core.config import logger
from db.auth import get_pool
from fastapi import Depends
from schemas.base import UserResponse



# class ApiTesting:
#     def __init__(self):
#         pass
#
#     async def get_list(self):
#
#         return {'Hello' : 'World1444'}
#
#
# @lru_cache()
# def get_apitesting_service() -> ApiTesting:
#     return ApiTesting()

class AuthServicetesting:
    """AuthService."""

    def __init__(self):
        pass

    async def get_by_id(self):
        return {'Hello': 'World'}



@lru_cache()
def get_auth_servicetesting() -> AuthServicetesting:
    """Get auth service.

    :param auth:
    :return:
    """
    return AuthServicetesting()


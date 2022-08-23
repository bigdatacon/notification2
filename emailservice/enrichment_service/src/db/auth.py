"""Auth."""

from typing import Optional

from asyncpg import Pool

pool: Optional[Pool] = None


async def get_pool() -> Pool:
    """Get pool."""
    return pool

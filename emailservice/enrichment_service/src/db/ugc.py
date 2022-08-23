"""UGC."""

from typing import Optional

from aiochclient import ChClient

client: Optional[ChClient] = None


async def get_client() -> ChClient:
    """Get client."""
    return client

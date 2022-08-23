"""Main."""

import asyncio

import core.config as config
from core.config import logger
import uvicorn
from aiochclient import ChClient
from aiohttp import ClientSession
from asyncpg import create_pool
from db import auth, movies, notification, ugc
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from routers import routes

app = FastAPI(
    debug=config.DEBUG,
    title=config.PROJECT_NAME,
    description=config.PROJECT_DESCRIPTION,
    version='0.0.1',
    default_response_class=ORJSONResponse,
    docs_url=config.API_DOC_URL,
    openapi_url=f'{config.API_DOC_URL}.json',
)


@app.on_event('startup')
async def startup():
    """Startup."""
    ugc.client = ChClient(session=ClientSession(), url=config.UGC_HOST)
    auth.pool, movies.pool, notification.client = await asyncio.gather(
        create_pool(dsn=config.AUTH_DSN_ASYNC),
        create_pool(dsn=config.MOVIES_DSN_ASYNC),
        create_pool(dsn=config.NOTIFICATIONS_DSN_ASYNC),
    )

    logger.info('API is UP')


@app.on_event('shutdown')
async def shutdown():
    """Shutdown."""
    await asyncio.gather(
        auth.pool.close(),
        movies.pool.close(),
        ugc.client.close(),
        notification.pool.close(),
    )
    logger.info('API is DOWN')


app.include_router(routes)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        debug=config.DEBUG,
        port=8080,
        reload=True,
        log_level=config.LOG_LEVEL.lower(),
    )

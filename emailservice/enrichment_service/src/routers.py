"""Routers."""

from api.v1 import advise, message, stats, user
from fastapi import APIRouter

routes = APIRouter()

routes.include_router(user.router, prefix='/api/v1/user', tags=['Enrichment API'])
routes.include_router(stats.router, prefix='/api/v1/stats', tags=['Enrichment API'])
routes.include_router(advise.router, prefix='/api/v1/advise', tags=['Enrichment API'])

routes.include_router(message.router, prefix='/api/v1/message', tags=['Enrichment API'])

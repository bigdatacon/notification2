"""Enrichment service User."""

import uuid
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Path

from core.config import logger
from schemas.base import UserResponse
from services.auth import AuthService, get_auth_service

router = APIRouter()


@router.get(
    '/{id:uuid}',
    response_model=UserResponse,
    summary='Информация о регистрации пользователя.',
    description='По идентификатору пользователя возвращает username и email.',
    response_description='Возвращает username и email пользователя.',
)
async def get_user(
        user_id: uuid.UUID = Path(
            ...,
            description='Идентификатор пользователя.',
            example='5d2d51ee-d7d6-447a-821d-b6093a6cf19f',
        ),
        auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    """Get user.

    :param user_id:
    :param auth_service:
    :return:
    """
    user = await auth_service.get_by_id(id=user_id)
    logger.info(f'Get user: {user}')

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User id not found.',
        )

    return UserResponse(username=user.username, email=user.email)

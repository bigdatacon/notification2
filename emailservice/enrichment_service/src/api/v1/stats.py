"""Enrichment service stats."""

from http import HTTPStatus

from core.config import logger
from fastapi import APIRouter, Depends, HTTPException
from schemas.base import StatsRequest, StatsResponse
from services.auth import AuthService, get_auth_service
from services.movies import MovieService, get_movie_service

router = APIRouter()


@router.post(
    '',
    response_model=StatsResponse,
    summary='Статистика пользователя за месяц.',
    description='По идентификатору пользователя возвращает статистику пользователя за месяц.',
    response_description="""Возвращает username и email пользователя, а так же жанры 
    просмотренных кинопроизведений за месяц.""",
)
async def get_stats(
        item: StatsRequest,
        auth_service: AuthService = Depends(get_auth_service),
        movie_service: MovieService = Depends(get_movie_service),
) -> StatsResponse:
    """Get stats.

    :param item:
    :param auth_service:
    :param movie_service:
    :return:
    """
    user = await auth_service.get_by_id(id=item.user_id)
    logger.info(f'Get stats user: {user}')

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User id not found',
        )

    genres = await movie_service.get_watched_genres(user_id=item.user_id)
    logger.info(f'Get stats genres: {genres}')

    result = StatsResponse(username=user.username, email=user.email, genres=genres)

    if not result:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
        )

    return result

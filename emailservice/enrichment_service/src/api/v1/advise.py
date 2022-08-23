"""Enrichment service advise."""

from http import HTTPStatus

from core.config import logger
from fastapi import APIRouter, Depends, HTTPException
from schemas.base import AdviseRequest, AdviseResponse
from services.auth import AuthService, get_auth_service
from services.movies import MovieService, get_movie_service

router = APIRouter()


@router.post(
    '',
    response_model=AdviseResponse,
    summary='Подборка фильмов за месяц.',
    description="""По идентификатору пользователя и списку идентификаторов кинопроизведений, проверяет
                не посмотрел ли пользователь уже эти кинопроизведения, и возвращает username и email, а так же
                возвращает список только 3 непросмотренных кинопроизведений.""",
    response_description='Возвращает username, email, список непросмотренных кинопроизведений.',
)
async def get_advise(
        item: AdviseRequest,
        auth_service: AuthService = Depends(get_auth_service),
        movie_service: MovieService = Depends(get_movie_service),
) -> AdviseResponse:
    """Get advise.

    :param item:
    :param auth_service:
    :param movie_service:
    :return:
    """
    user = await auth_service.get_by_id(id=item.user_id)
    logger.info(f'Get advise user: {user}')

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User id not found.',
        )

    movies = await movie_service.get_movies(user_id=item.user_id, movie_ids=item.movies)
    logger.info(f'Get advise movies: {movies}')

    result = AdviseResponse(username=user.username, email=user.email, movies=movies)
    logger.info(f'Get advise result: {result}')

    if not result:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
        )

    return result

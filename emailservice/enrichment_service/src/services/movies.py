"""Movies service."""

import uuid
from typing import List

from aiochclient import ChClient
from asyncpg import Pool
from core.config import logger
from db.movies import get_pool
from db.ugc import get_client
from fastapi import Depends
from schemas.base import GenreName, Movie, MovieId


class MovieService:
    """Movie Service."""

    def __init__(self, movie: Pool, ugc: ChClient):
        """Initialization.

        :param movie:
        :param ugc:
        """
        self.movie = movie
        self.ugc = ugc

    async def get_movies_by_sql(self, sql: str) -> List:
        """Get movies by sql.

        :param sql:
        :return:
        """
        rows = await self.ugc.fetch(sql)
        return [MovieId.parse_obj(dict(row)) for row in rows]

    async def get_watched_genres(self, user_id: uuid.UUID) -> List[GenreName]:
        """Get watched genres.

        :param user_id:
        :return:
        """
        movies = await self.get_movies_by_sql(
            sql=f"SELECT movie_id FROM user_events WHERE user_id = '{user_id}'"
        )

        movie_uuids = '::uuid,'.join(f"'{movie.movie_id}'" for movie in movies)
        logger.info(f'movie_uuids: {movie_uuids}')

        async with self.movie.acquire() as con:
            rows = await con.fetch(f"""SELECT genre.name as genre_name FROM content.filmwork
                JOIN content.filmwork_genre ON content.filmwork.uuid = content.filmwork_genre.filmwork_id
                JOIN content.genre ON content.filmwork_genre.genre_id = content.genre.uuid
                WHERE filmwork.uuid IN ({movie_uuids});""")
            logger.info(f'rows: {rows}')

            genres = [GenreName.parse_obj(dict(row)) for row in rows]
            logger.info(f'genres: {genres}')

        return genres

    async def get_movies(
            self, user_id: uuid.UUID, movie_ids: List[uuid.UUID]
    ) -> List[Movie]:
        """Get movies.

        :param user_id:
        :param movie_ids:
        :return:
        """
        if len(movie_ids) == 0:
            return []

        movie_uuids = ','.join(f"'{movie_id}'" for movie_id in movie_ids)
        logger.info(f'movie_uuids: {movie_uuids}')

        movies = await self.get_movies_by_sql(
            sql=f"SELECT movie_id FROM user_events WHERE user_id = '{user_id}' AND movie_id NOT IN ({movie_uuids})"
        )
        movie_uuids = '::uuid,'.join(f"'{movie.movie_id}'" for movie in movies)
        logger.info(f'movie _uuids: {movie_uuids}')

        if len(movie_uuids) == 0:
            return []

        async with self.movie.acquire() as con:
            rows = await con.fetch(
                f"""SELECT filmwork.uuid as movie_id, filmwork.title as movie_title 
                FROM content.filmwork WHERE filmwork.uuid IN ({movie_uuids});"""
            )
            logger.info(f'rows: {rows}')

            movies = [Movie.parse_obj(dict(row)) for row in rows]
            logger.info(f'movies_new: {movies}')

        return movies


# @lru_cache()
def get_movie_service(
        movie: Pool = Depends(get_pool),
        ugc: ChClient = Depends(get_client),
) -> MovieService:
    """Get movie service.

    :param movie:
    :param ugc:
    :return:
    """
    return MovieService(movie=movie, ugc=ugc)

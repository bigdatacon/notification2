"""Schema Base."""

import uuid
from enum import Enum
from typing import Any, Dict, List

from pydantic import BaseModel, EmailStr


class MovieId(BaseModel):
    """Movie Id."""

    movie_id: uuid.UUID


class Movie(MovieId):
    """Movie."""

    movie_title: str


class MovieName(BaseModel):
    """Movie Name."""

    movie_name: str


class GenreName(BaseModel):
    """Genre Name."""

    genre_name: str


class UserResponse(BaseModel):
    """User Response."""

    id: uuid.UUID
    username: str
    email: EmailStr


class AdviseRequest(BaseModel):
    """Advise Request."""

    user_id: uuid.UUID
    movies: List[uuid.UUID]


class AdviseResponse(UserResponse):
    """Advise Response."""

    movies: List[Movie]


class StatsRequest(BaseModel):
    """Stats Request."""

    user_id: uuid.UUID


class StatsResponse(UserResponse):
    """Stats Response."""

    genres: List[GenreName]


class TemplateName(Enum):
    """Template Name."""

    USER_REGISTERED = 'user_registered'
    USER_MONTH_STATISTIC = 'user_month_statistics'
    LAST_WEEK_NEW_MOVIES = 'last_week_new_movies'


class Template(BaseModel):
    """Template."""

    template_text: str
    send_via_email: bool
    send_via_sms: bool


class Message(BaseModel):
    """Message."""

    template_name: str
    user_ids: List[uuid.UUID]
    data: Dict[str, Any]


class EnrichedMessage(BaseModel):
    """EnrichedMessage."""

    template: str
    user_data: Dict[uuid.UUID, dict[str, str]]
    shipping_methods: List[str]

"""Message."""

from http import HTTPStatus
from typing import List

from core import config
from fastapi import APIRouter, Depends, HTTPException
from schemas.base import EnrichedMessage, Message, Template, TemplateName
from services.auth import AuthService, get_auth_service
from services.movies import MovieService, get_movie_service
from services.notifications import (NotificationService,
                                    get_notification_service)

router = APIRouter()


def craft_shipment_methods(template: Template) -> List[str]:
    """Craft shipment methods.

    :param template:
    :return:
    """
    methods = []
    if template.send_via_email:
        methods.append(config.EMAIL_SHIPMENT_METHOD)
    if template.send_via_sms:
        methods.append(config.SMS_SHIPMENT_METHOD)
    return methods


@router.post(
    '/',
    response_model=EnrichedMessage,
    summary='Обогащение сообщения информацией из базы данных',
    description='Принимает сообщение, по имени шаблона забирает из бд нужные данные',
    response_description='Возвращает обогащенную информацию',
)
async def enrich_msg(
        item: Message,
        auth_service: AuthService = Depends(get_auth_service),
        notification_service: NotificationService = Depends(get_notification_service),
        movie_service: MovieService = Depends(get_movie_service),
) -> EnrichedMessage:
    """Enrich msg.

    :param item:
    :param auth_service:
    :param notification_service:
    :param movie_service:
    :return:
    """
    template = await notification_service.get_notification_template(item.template_name)
    if item.template_name == TemplateName.USER_REGISTERED.value:
        users_info = await auth_service.get_many_by_ids(item.user_ids)
        response = EnrichedMessage(
            template=template.template_text,
            user_data={
                user.id: {
                    'email': user.email,
                    'username': user.username
                }
                for user in users_info
            },
            shipping_methods=craft_shipment_methods(template)
        )

    elif item.template_name == TemplateName.USER_MONTH_STATISTIC.value:
        users_info = await auth_service.get_many_by_ids(item.user_ids)
        response = EnrichedMessage(
            template=template.template_text,
            user_data={
                user.id: {
                    'email': user.email,
                    'username': user.username,
                    'genres': await movie_service.get_watched_genres(user.id)
                }
                for user in users_info
            },
            shipping_methods=craft_shipment_methods(template)
        )

    elif item.template_name == TemplateName.LAST_WEEK_NEW_MOVIES.value:
        users_info = await auth_service.get_many_by_ids(item.user_ids)
        response = EnrichedMessage(
            template=template.template_text,
            user_data={
                user.id: {
                    'email': user.email,
                    'username': user.username,
                    'movies': await movie_service.get_movies(user_id=user.id, movie_ids=item.data.get('new_movie_ids'))
                }
                for user in users_info
            },
            shipping_methods=craft_shipment_methods(template)
        )

    else:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Template name not found.',
        )
    return response

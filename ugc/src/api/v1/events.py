from http import HTTPStatus

from api.v1.utils import EventEnum
from core.config import settings
from fastapi import APIRouter, Depends, HTTPException, Response
from kafka import errors
from models.events import Event
from services.broker.producer import KafkaProducer, get_producer
from utils import auth

router = APIRouter()
auth_handler = auth.AuthHandler()

kafka_exceptions = (errors.KafkaConnectionError, errors.KafkaTimeoutError, errors.KafkaUnavailableError)


@router.get(path='/produce2')
async def kafka_produce2():
    raise ZeroDivisionError


@router.post(
    path='/produce/{movie_id}/{event_type}',
    response_model=Event,
    summary='Отправка события.',
    description='Отправка события в топик kafka',
    response_description='Событие',
)
async def kafka_produce(
    movie_id: str,
    event_type: EventEnum,
    event: int,
    producer: KafkaProducer = Depends(get_producer),
    _user: dict = Depends(auth_handler.auth_wrapper),
):
    if (settings.permission.User.value in _user['claims'].get('permissions')) or _user['claims'].get('is_super'):
        try:
            event = await producer.produce(movie_id, event, event_type.value, user_id=_user['user_id'])
        except kafka_exceptions:
            return HTTPException(detail='Storage is unavailable', status_code=HTTPStatus.BAD_GATEWAY)
        return event
    return Response('Permission denied', HTTPStatus.FORBIDDEN)


@router.post(
    path='/batch-produce',
    summary='Отправка пачки событий.',
    description='Отправка пачки событий в топик kafka',
    response_description='Пачка событий',
)
async def kafka_batch_produce(
    batch_size: int,
    producer: KafkaProducer = Depends(get_producer),
    _user: dict = Depends(auth_handler.auth_wrapper),
):
    if (settings.permission.Moderator.value in _user['claims'].get('permissions')) or _user['claims'].get('is_super'):
        try:
            await producer.batch_produce(batch_size)
        except kafka_exceptions:
            return HTTPException(detail='Storage is unavailable', status_code=HTTPStatus.BAD_GATEWAY)
        return {'msg': 'Events saved'}
    return Response('Permission denied', HTTPStatus.FORBIDDEN)

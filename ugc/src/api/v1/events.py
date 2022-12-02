from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from kafka.errors import KafkaConnectionError, KafkaTimeoutError, KafkaUnavailableError
from models.events import Event
from services.broker.produser import KafkaProducer, get_producer

router = APIRouter()

kafka_exceptions = (KafkaConnectionError, KafkaTimeoutError, KafkaUnavailableError)


@router.post(
    path='produce/{movie_id}/{event_type}',
    response_model=Event,
    summary='Отправка события.',
    description='Отправка события в топик kafka',
    response_description='Событие',
)
async def kafka_produce(
    movie_id: str | UUID,
    event_type: str,
    event: int,
    producer: KafkaProducer = Depends(get_producer),
):
    try:
        event = await producer.produce(movie_id, event, event_type)
    except kafka_exceptions:
        return HTTPException(detail='Storage is unavailable', status_code=HTTPStatus.BAD_GATEWAY)
    return event


@router.post(
    path='batch-produce',
    #response_model=Event,
    summary='Отправка пачки событий.',
    description='Отправка пачки событий в топик kafka',
    response_description='Пачка событий',
)
async def kafka_produce(batch_size: int, producer: KafkaProducer = Depends(get_producer)):
    try:
        await producer.batch_produce(batch_size)
    except kafka_exceptions:
        return HTTPException(detail='Storage is unavailable', status_code=HTTPStatus.BAD_GATEWAY)
    return {'msg': 'Events saved'}

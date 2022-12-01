from uuid import UUID

from fastapi import APIRouter, Depends
from models.events import Event
from services.broker.produser import KafkaProducer, get_producer

router = APIRouter()


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
    await producer.produce(movie_id, event, event_type)


@router.post(
    path='batch-produce',
    response_model=Event,
    summary='Отправка пачки событий.',
    description='Отправка пачки событий в топик kafka',
    response_description='Пачка событий',
)
async def kafka_produce(batch_size: int, producer: KafkaProducer = Depends(get_producer)):
    await producer.batch_produce(batch_size)

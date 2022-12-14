from enum import Enum
from http import HTTPStatus


class EventEnum(str, Enum):
    views = 'views'
    rating = 'rating'


def response_model(data, message: str) -> dict:
    return {
        'data': data,
        'code': HTTPStatus.OK,
        'message': message,
    }


class NotFoundError(Exception):
    ...

import re
from typing import Optional

import jwt
from core.config import settings
from core.logger import get_logger
from fastapi import FastAPI, Response
from jwt import DecodeError, ExpiredSignatureError

logger = get_logger(__name__)


def _parse_auth_header(
    auth_header: str,
    access_token_title: str = 'Bearer',
    refresh_token_title: str = 'Refresh',
) -> dict:
    """Parses a Authorization/Authentication http header and extracts the access + request
    tokens if present.
    Example header:
    "Authorization: Bearer AAA, Refresh BBB"
    """

    def _match_token(token_title: str) -> Optional[str]:
        expression = re.escape(token_title) + r' ([^\s,]+)'
        match = re.search(expression, auth_header)
        try:
            return match.group(1)
        except (AttributeError, IndexError):
            return None

    tokens = {'access_token': _match_token(access_token_title), 'refresh_token': _match_token(refresh_token_title)}
    return tokens


def parse_header(auth_header) -> dict:
    jwt_token = _parse_auth_header(auth_header)['access_token']
    try:
        decoded_jwt = jwt.decode(
            jwt=jwt_token,
            key=settings.jwt.SECRET_KEY,
            algorithms=[settings.jwt.ALGORITHM],
        )
        return {
            'user_id': decoded_jwt.identity,
            'claims': decoded_jwt.additional_claims,
        }
    except (DecodeError, ExpiredSignatureError) as ex:
        logger.exception('Ошибка при проверке access_token: \n %s', str(ex))

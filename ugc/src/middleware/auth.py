from http import HTTPStatus

from core.config import settings
from fastapi import FastAPI, Request
from fastapi.responses import Response
from utils.auth import parse_header


def auth_middleware(app: FastAPI):
    @app.middleware('http')
    async def check_jwt(request: Request, call_next):
        auth_header = request.headers.get('Authorization')
        if auth_header in None:
            return Response('Authorization header is missing', HTTPStatus.UNAUTHORIZED)
        claims = parse_header(auth_header)['claims']
        if claims.get('is_super'):
            return await call_next(request)

        if 'http://fastapi:8000/ugc_api/v1/event/produce' in str(request.url):
            if settings.permission.User in claims.get('permissions'):
                return await call_next(request)
            return Response('Permission denied', HTTPStatus.FORBIDDEN)

        if 'http://fastapi:8000/ugc_api/v1/event/batch-produce' in str(request.url):
            if settings.permission.Moderator in claims.get('permissions'):
                return await call_next(request)
            return Response('Permission denied', HTTPStatus.FORBIDDEN)
        return await call_next(request)

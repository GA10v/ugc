import logging

import sentry_sdk
import uvicorn
from aiokafka import AIOKafkaProducer
from api.v1 import bookmarks, events, ratings, reviews
from core.config import settings
from core.logger import LOGGING
from db import mongo
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from middleware.auth import auth_middleware
from middleware.logger import logging_middleware
from motor.motor_asyncio import AsyncIOMotorClient
from sentry_sdk.integrations.fastapi import FastApiIntegration
from services.broker import producer

sentry_sdk.init(dsn=settings.logging.SENTRY_DSN, integrations=[FastApiIntegration()])

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

logging_middleware(app=app)


@app.on_event('startup')
async def startup_event():
    producer.aioproducer = AIOKafkaProducer(**settings.kafka.producer_conf)
    client = AsyncIOMotorClient(settings.mongo.uri)
    mongo.mongo = client[settings.mongo.DB]
    await producer.aioproducer.start()


@app.on_event('shutdown')
async def shutdown_event():
    mongo.mongo.close()
    await producer.aioproducer.stop()


if not settings.debug.DEBUG:
    auth_middleware(app=app)

app.include_router(events.router, prefix=settings.fastapi.EVENT_PREFIX, tags=['events'])
app.include_router(bookmarks.router, prefix=settings.fastapi.BOOKMARK_PREFIX, tags=['bookmarks'])
app.include_router(ratings.router, prefix=settings.fastapi.RATING_PREFIX, tags=['ratings'])
app.include_router(reviews.router, prefix=settings.fastapi.REVIEW_PREFIX, tags=['reviews'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8001, log_config=LOGGING, log_level=logging.DEBUG)

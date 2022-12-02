import asyncio
import logging

import uvicorn
from aiokafka import AIOKafkaProducer
from api.v1 import events
from core import kafka
from core.config import settings
from core.logger import LOGGING
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from middleware.auth import auth_middleware
from services.broker import produser

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup_event():
    produser.aioproducer = AIOKafkaProducer(**settings.kafka.producer_conf)
    await produser.aioproducer.start()


@app.on_event('shutdown')
async def shutdown_event():
    await produser.aioproducer.stop()


# auth_middleware(app=app)

app.include_router(events.router, prefix='/ugc_api/v1/event', tags=['events'])

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8001, log_config=LOGGING, log_level=logging.DEBUG)

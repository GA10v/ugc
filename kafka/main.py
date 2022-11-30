import asyncio
import json
import logging
from uuid import UUID


import uvicorn
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from fastapi import FastAPI
from kafka.errors import KafkaConnectionError
from pydantic import BaseModel, StrictStr


LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DEFAULT_HANDLERS = ["console"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": LOG_FORMAT},
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {"handlers": LOG_DEFAULT_HANDLERS, "level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
    "root": {"level": "INFO", "formatter": "verbose", "handlers": LOG_DEFAULT_HANDLERS},
}

app = FastAPI()
loop = asyncio.get_event_loop()

KAFKA_INSTANCE = "localhost:9092"
aioproducer = AIOKafkaProducer(
    loop=loop,
    bootstrap_servers=KAFKA_INSTANCE
)


@app.on_event("startup")
async def startup_event():
    await aioproducer.start()
    # await consumer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await aioproducer.stop()
    # await consumer.stop()


class ViewsMessage(BaseModel):
    user_id: UUID
    film_id: UUID
    timestamp: int


@app.post("/producer/{topicname}")
async def kafka_produce(msg: ViewsMessage, topicname: str):
    try:
        await aioproducer.send_and_wait(
            topic=topicname,
            value=json.dumps(msg.timestamp).encode("utf-8"),
            key=':'.join([str(msg.user_id), str(msg.film_id)]).encode("utf-8")
        )
    except KafkaConnectionError as exc:
        response = {'msg': str(exc)}
        return response

    response = {'msg': 'successful'}
    return response


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        log_config=LOGGING,
        log_level=logging.DEBUG
    )

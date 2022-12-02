FROM python:3.10

ARG PROJECT_ENV

WORKDIR /app/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y libpq-dev wait-for-it && \
    apt-get clean

RUN pip install --no-cache-dir poetry==1.1.14

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry config virtualenvs.create false && \
    poetry install $(test "$PROJECT_ENV" = production && echo "--no-dev") --no-interaction --no-ansi

# To prevent error: ModuleFoundError pkg-resources
RUN pip install --upgrade pip
RUN pip install --force-reinstall -U setuptools

COPY ugc/src .
COPY .flake8 .flake8

ENTRYPOINT ["gunicorn", "-w 4", "-b 0.0.0.0:8001", "-k uvicorn.workers.UvicornWorker", "main:app"]
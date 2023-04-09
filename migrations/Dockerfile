FROM python:3.9.16-slim-buster

WORKDIR /app

COPY ./migrations ./migrations 
COPY ./db_toolkit ./db_toolkit 

WORKDIR /app/migrations

RUN pip install poetry
RUN poetry install 

WORKDIR /app/migrations/src

CMD [ "poetry", "run", "alembic", "upgrade", "head" ]
FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./src ./src
COPY ./alembic ./alembic
COPY alembic.ini alembic.ini
COPY app.sh app.sh
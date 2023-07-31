FROM docker.io/python:3-alpine AS base

WORKDIR /usr/src/app
RUN apk add --no-cache --virtual .build-deps gcc musl-dev
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY ./src .

FROM base AS dev

ENV FLASK_ENV development
CMD [ "python", "app.py" ]

FROM base AS prod

RUN pip install gunicorn
CMD [ "gunicorn", "--bind", "0.0.0.0:80", "app:app" ]

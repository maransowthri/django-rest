FROM python:3.10.0a5-alpine3.13
MAINTAINER Maran Sowthri Kalailingam

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D kmaran
USER kmaran

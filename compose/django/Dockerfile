FROM python:3.6.11-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y \
  # psycopg2 dependencies
  && apt-get install gcc -y \
  && apt-get install libpq-dev -y

RUN addgroup --system askru \
    && adduser --system --group askru --shell /bin/sh

WORKDIR /home/askru/

RUN mkdir -p /var/askru/static/
RUN mkdir -p /var/askru/media/

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/requirements.txt \
    && rm -rf /requirements

COPY ./compose/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start
RUN chown askru /start

COPY ./config /askru/config
COPY ./askru /askru/askru
COPY ./polls /askru/polls
COPY ./manage.py /askru

RUN chown -R askru /askru
RUN chown -R askru /var/askru/static
RUN chown -R askru /var/askru/media

USER askru

WORKDIR /askru


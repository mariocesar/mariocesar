FROM python:3.9-slim

COPY requirements.txt /requirements.txt

RUN set -eux \
    && pip install --no-cache-dir -r /requirements.txt

WORKDIR /app

COPY . /app

RUN set -eux \
    && python /app/main.py

CMD python -m http.server --bind 0.0.0.0 --directory /app/out

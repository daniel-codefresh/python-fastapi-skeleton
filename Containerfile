FROM python:3.11-alpine AS builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_HOME="/opt/poetry"

ENV PATH="$POETRY_HOME/bin:$PATH"
WORKDIR /build

RUN apk update && \
    apk add git gcc curl && \
    curl -sSL https://install.python-poetry.org | python3 -

COPY poetry.lock pyproject.toml  ./

RUN poetry export \
    --without-hashes \
    -f requirements.txt \
    --output requirements.txt \
    --only main

RUN pip install --prefix /local --no-cache-dir pip && \
    pip install --prefix /local -I --no-cache-dir -r requirements.txt


FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1
RUN apk update && apk add just tzdata
RUN cp /usr/share/zoneinfo/UTC /etc/localtime

RUN adduser --home /app --disabled-password app
COPY --from=builder /local/ /usr/local
COPY --chown=app:app . /app
USER app
WORKDIR /app

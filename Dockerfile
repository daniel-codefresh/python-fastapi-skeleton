FROM python:3.11.4-slim-bullseye as base
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app


FROM base as builder
# pip
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
     # poetry
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_HOME=/opt/poetry \
    POETRY_VERSION=1.5.1
RUN pip install poetry==1.5.1
COPY pyproject.toml poetry.lock /app/
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-interaction --no-ansi --no-root


FROM base as runtime

# Allow running in rootless mode
RUN useradd -ms /bin/bash app
USER app

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY ./src /app
WORKDIR /app

CMD ["uvicorn", "python_project_skeleton.main:app", "--host", "0.0.0.0", "--port", "8000"]

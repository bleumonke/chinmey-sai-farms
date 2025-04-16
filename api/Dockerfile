FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y gcc libpq-dev curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
COPY . .
EXPOSE 8000

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

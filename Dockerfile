FROM ghcr.io/astral-sh/uv:0.9.13-python3.13-trixie

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-install-project --no-dev

COPY . .

RUN uv sync --locked --no-dev

CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn task.main:app --host 0.0.0.0 --port 8000"]
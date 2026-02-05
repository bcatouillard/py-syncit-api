# Stage 1 - Build requirements.txt
FROM python:3.12-alpine AS build_stage
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY uv.lock .
COPY pyproject.toml .
RUN uv export -v --no-hashes --no-dev > requirements.txt

# Stage 2 - Install all packages and start the API
FROM python:3.12-alpine AS api
WORKDIR /app

COPY ./src/ ./src
COPY pyproject.toml .
COPY README.md .
COPY --from=build_stage /app/requirements.txt .

ARG AUTHED_ARTIFACT_REG_URL
ENV PYTHONUNBUFFERED=1

RUN pip3 install --no-cache --upgrade pip setuptools

USER 1001

EXPOSE 8000

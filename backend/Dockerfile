# syntax=docker/dockerfile:1

FROM python:3.12-alpine AS builder

WORKDIR /app

# Build deps needed to compile the `cryptography` package on musl (removed from final image)
RUN apk add --no-cache build-base libffi-dev openssl-dev cargo rust

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt "uvicorn[standard]"


FROM python:3.12-alpine AS runtime

RUN apk add --no-cache libffi openssl \
    && addgroup -S app && adduser -S app -G app

WORKDIR /app

COPY --from=builder /install /usr/local
COPY . .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings

RUN chown -R app:app /app

USER app

EXPOSE 8000

CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--workers", "3"]

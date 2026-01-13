FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m venv .venv \
    && .venv/bin/pip install --upgrade pip \
    && .venv/bin/pip install -r requirements.txt \
    && .venv/bin/pip install gunicorn \
    && .venv/bin/python -m spacy download en_core_web_sm

RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY . .

RUN mkdir -p /app/logs /app/static /app/media \
    && chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "wingman.wsgi:application", "--bind", "0.0.0.0:8000"]
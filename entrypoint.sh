#!/bin/sh

set -e

if echo "$DATABASE_BASE_URL" | grep -q "postgre"; then
    echo "Waiting for PostgreSQL..."
    
    DB_HOST=$(python -c "from urllib.parse import urlparse; print(urlparse('$DATABASE_BASE_URL').hostname)")
    DB_PORT=$(python -c "from urllib.parse import urlparse; print(urlparse('$DATABASE_BASE_URL').port or 5432)")

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.5
    done
    echo "PostgreSQL started at $DB_HOST:$DB_PORT"
fi

if echo "$@" | grep -q "gunicorn"; then
    echo "Running initialization tasks..."
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput --clear
fi

exec "$@"
#!/bin/sh

set -e

if echo "$DATABASE_BASE_URL" | grep -q "postgre"; then
    echo "Waiting for PostgreSQL..."
    
    DB_HOST=$(echo $DATABASE_BASE_URL | sed -e 's|^.*@||' -e 's|/.*$||' -e 's|:.*$||')
    DB_PORT=$(echo $DATABASE_BASE_URL | sed -e 's|^.*@||' -e 's|/.*$||' -e 's|^.*:||')
    
    if [ "$DB_PORT" = "$DB_HOST" ]; then
        DB_PORT=5432
    fi

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.5
    done
    echo "PostgreSQL started"
fi

if echo "$@" | grep -q "gunicorn"; then
    echo "Running initialization tasks for Web Container..."
    
    echo "Applying migrations..."
    python manage.py migrate --noinput

    echo "Collecting static files..."
    python manage.py collectstatic --noinput --clear
fi

exec "$@"
#!/bin/sh

set -e

if echo "$DATABASE_BASE_URL" | grep -q "postgres://"; then
    echo "Waiting for PostgreSQL..."
    DB_HOST=$(echo $DATABASE_BASE_URL | sed -e 's|^.*@||' -e 's|/.*$||' -e 's|:.*$||')
    DB_PORT=$(echo $DATABASE_BASE_URL | sed -e 's|^.*@||' -e 's|/.*$||' -e 's|^.*:||')
    [ -z "$DB_PORT" ] && DB_PORT=5432
    
    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.5
    done
    echo "PostgreSQL started"
fi

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

exec "$@"
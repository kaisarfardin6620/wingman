#!/bin/sh

set -e

echo "Waiting for Redis..."
REDIS_HOST=$(python -c "
import os
url = os.environ.get('REDIS_URL', 'redis://redis:6379')
from urllib.parse import urlparse
p = urlparse(url)
print(p.hostname)
")
REDIS_PORT=$(python -c "
import os
url = os.environ.get('REDIS_URL', 'redis://redis:6379')
from urllib.parse import urlparse
p = urlparse(url)
print(p.port or 6379)
")

while ! nc -z $REDIS_HOST $REDIS_PORT; do
    sleep 0.5
done
echo "Redis ready at $REDIS_HOST:$REDIS_PORT"

echo "Waiting for PgBouncer..."
PGBOUNCER_HOST=$(python -c "
import os
url = os.environ.get('DATABASE_BASE_URL', '')
from urllib.parse import urlparse
p = urlparse(url)
print(p.hostname)
")
PGBOUNCER_PORT=$(python -c "
import os
url = os.environ.get('DATABASE_BASE_URL', '')
from urllib.parse import urlparse
p = urlparse(url)
print(p.port or 5432)
")

RETRIES=30
while ! nc -z $PGBOUNCER_HOST $PGBOUNCER_PORT; do
    RETRIES=$((RETRIES - 1))
    if [ $RETRIES -eq 0 ]; then
        echo "ERROR: PgBouncer not available after 30 retries. Exiting."
        exit 1
    fi
    echo "PgBouncer not ready yet... ($RETRIES retries left)"
    sleep 1
done
echo "PgBouncer ready at $PGBOUNCER_HOST:$PGBOUNCER_PORT"

if echo "$@" | grep -q "gunicorn"; then
    echo "Running migrations..."
    python manage.py migrate --noinput

    echo "Collecting static files..."
    python manage.py collectstatic --noinput --clear

    echo "Django setup complete."
fi

echo "Starting: $@"
exec "$@"
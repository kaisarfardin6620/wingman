#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Apply database migrations
python manage.py migrate

# Ensure proper permissions for static and media files
chmod -R 755 /app/static /app/media

# Ensure proper permissions for log files
mkdir -p /app/logs
chmod -R 755 /app/logs

# Collect static files (if applicable)
python manage.py collectstatic --noinput

# Start the application
exec "$@"
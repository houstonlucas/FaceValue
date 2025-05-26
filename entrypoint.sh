#!/bin/bash

# entrypoint.sh for Docker
# Exit on error
set -e

# Wait for Postgres
echo "Waiting for Postgres to become available..."
until python - << 'PYTHON'
import sys, psycopg2, os
try:
    psycopg2.connect(
        dbname=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD'),
        host=os.environ.get('POSTGRES_HOST'),
        port=os.environ.get('POSTGRES_PORT')
    )
except Exception:
    sys.exit(1)
sys.exit(0)
PYTHON
do
    echo "Postgres is unavailable - sleeping"
    sleep 1
done
echo "PostgreSQL started"

# Run migrations and collectstatic
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Launch the application
exec "$@"

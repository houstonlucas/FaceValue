#!/bin/bash

# entrypoint.sh for Docker
# Exit on error
set -e

# Wait for database if using PostgreSQL
if [ "$POSTGRES_HOST" != "" ]; then
    echo "Waiting for Postgres to become available..."
    until python - << 'PYTHON'
import sys, os
try:
    import psycopg2
    psycopg2.connect(
        dbname=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD'),
        host=os.environ.get('POSTGRES_HOST'),
        port=os.environ.get('POSTGRES_PORT', '5432')
    )
except Exception as e:
    print(f"Database connection failed: {e}")
    sys.exit(1)
sys.exit(0)
PYTHON
    do
        echo "Postgres is unavailable - sleeping"
        sleep 1
    done
    echo "PostgreSQL started"
else
    echo "Using SQLite database"
fi

# Run migrations and collectstatic
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Execute the main command
exec "$@"

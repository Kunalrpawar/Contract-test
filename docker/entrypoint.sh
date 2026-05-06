#!/bin/bash
# Entrypoint script for Docker container

echo "Waiting for database to be ready..."
sleep 10

echo "Initializing database..."
python init_db.py

echo "Starting application..."
exec python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

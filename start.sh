#!/bin/bash

mkdir -p uploads

# Sleep to wait the database docker mount
sleep 10

echo -e "Syncing database..."
python3 -m alembic upgrade head
echo -e "Database synced"

# Just to start the authorization service
python3 setup.py
python3 -m uvicorn services.main:app --reload --host 0.0.0.0 --port 5000  
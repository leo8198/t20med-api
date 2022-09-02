#!/bin/bash

# Just to start the authorization service
python3 setup.py
python3 -m uvicorn services.authentication.routers.main:app --reload --port 5000  
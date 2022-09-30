#!/bin/bash

python3 -m uvicorn appointments.main:app --reload --host 0.0.0.0 --port 5001 
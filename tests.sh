#!/bin/bash

# Change to the tests env
mv .env .env.tmp
mv .env.test .env

# Run the tests
pytest tests/authentication_test.py \
       tests/users_test.py  \
       tests/doctors_test.py \
       tests/agenda_test.py

# Go back to the developement env
mv .env .env.test
mv .env.tmp .env
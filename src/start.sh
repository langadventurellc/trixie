#! /usr/bin/env bash

# Run prestart from the app directory
cd app
python app_prestart.py

# Run uvicorn from parent directory to handle relative imports correctly
cd ..
exec uvicorn app.main:app --host 0.0.0.0 --port 80

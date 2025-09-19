#! /usr/bin/env bash

# Run prestart from the app directory
cd app
python app_prestart.py

# Run uvicorn from parent directory to handle relative imports correctly
cd ..

# Check if SSL certificates exist and start with HTTPS if available
if [ -f "/certs/trixie.crt" ] && [ -f "/certs/trixie.key" ]; then
    echo "SSL certificates found, starting with HTTPS support..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 443 --ssl-keyfile=/certs/trixie.key --ssl-certfile=/certs/trixie.crt
else
    echo "SSL certificates not found, starting with HTTP only..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 80
fi

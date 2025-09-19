#!/bin/bash

# Create certificates directory if it doesn't exist
mkdir -p certs

# Generate self-signed certificate for localhost
openssl req -x509 -newkey rsa:4096 \
    -keyout certs/trixie.key \
    -out certs/trixie.crt \
    -days 365 \
    -nodes \
    -subj "/C=US/ST=Development/L=Local/O=Development/CN=localhost" \
    -addext "subjectAltName=DNS:localhost,DNS:127.0.0.1,IP:127.0.0.1"

echo "SSL certificates generated in ./certs/"
echo "- Certificate: certs/trixie.crt"
echo "- Private key: certs/trixie.key"
echo ""
echo "Run 'docker-compose up --build' to start the API with HTTPS support"
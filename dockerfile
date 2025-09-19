FROM ghcr.io/langadventurellc/docker-gcp-poetry:3.12 AS package-install
WORKDIR /tmp

COPY ./poetry.lock* ./pyproject.toml /tmp/
RUN poetry self add poetry-plugin-export
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

FROM python:3.12
WORKDIR /code
COPY --from=package-install /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=package-install /usr/local/bin /usr/local/bin
COPY ./src /code/app

WORKDIR /code/app
RUN chmod +x ./start.sh
CMD ["./start.sh"]
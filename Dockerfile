FROM python:3.9.19-slim-bookworm

ARG GIT_COMMIT=placeholder
ENV GIT_COMMIT=$GIT_COMMIT

# RUN apk add --no-cache libcurl curl-dev build-base
# RUN apk add --no-cache libcurl curl-dev build-base linux-headers libffi-dev

COPY requirements/requirements.txt requirements/requirements.txt

RUN python -m pip install -r requirements/requirements.txt

COPY src/. .

COPY docker-entrypoint.sh docker-entrypoint.sh

# COPY request-api/makefile makefile

ENTRYPOINT ["./docker-entrypoint.sh"]

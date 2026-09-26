FROM python:3.13-slim-bookworm

ARG GIT_COMMIT=placeholder
ENV GIT_COMMIT=$GIT_COMMIT

# update debian packages, worth the trade off of them changing as it will ensure security updates
RUN apt-get update \
    && apt-get upgrade -y \
    # remove the apt cache to reduce image size
    && rm -rf /var/lib/apt/lists/*

COPY requirements/requirements.txt requirements/requirements.txt
COPY requirements/test_requirements.txt requirements/test_requirements.txt

RUN python -m pip install -r requirements/requirements.txt

RUN python -m pip install -r requirements/test_requirements.txt

# Pre-install the DuckDB extensions the app needs at runtime. Both are fetched
# from http://extensions.duckdb.org (port 80) on first use, so downloading them
# at build time keeps the container off the network on its first S3 query.
RUN python -c "import duckdb; con = duckdb.connect(); con.execute('INSTALL httpfs'); con.execute('INSTALL aws')"

COPY src/. .

COPY tests/. tests/.

COPY docker-entrypoint.sh docker-entrypoint.sh

# COPY request-api/makefile makefile

ENTRYPOINT ["./docker-entrypoint.sh"]

# dockerfile for ia.com.mx test project
# This file is used to build the docker image for the project

# Use the official Python image from the Docker Hub
FROM python:3.11.9

LABEL authors="robertuj"

# configure workdir and save path in the environment variable
ENV APP_HOME=/usr/src/app
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ="America/Mexico_City"

# Update and install dependencies linux bullseye version
RUN set -eux; \
    apt-get update -y && apt-get install -y \
    curl \
    vim \
    gcc \
    gettext \
    git \
    libpq-dev \
    make \
    musl-dev \
    postgresql-client \
    python3-dev \
    tzdata \
    build-essential \
    libffi-dev \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add poetry official installation version 1.8.3 \
RUN set -ex \
    && pip install poetry==1.8.3 \
    && poetry config virtualenvs.create false

# copy the poetry configuration file \
COPY poetry.lock pyproject.toml  $APP_HOME

# Allow installing dev dependencies to run tests
#ARG INSTALL_DEV=true
#RUN sh -c "if [ $INSTALL_DEV == 'true' ]; then poetry install --no-root; else poetry install --no-root --only main; fi"
RUN poetry install --no-root

# install dbmate for migrations and set execution permissions
RUN curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64
RUN chmod +x /usr/local/bin/dbmate

# copy the project files
COPY . .

# Add +x permissions to the entrypoint.sh file
RUN chmod +x entrypoint.sh

# run the entrypoint.sh file
ENTRYPOINT ["./entrypoint.sh"]

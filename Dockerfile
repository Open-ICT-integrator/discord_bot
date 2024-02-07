# syntax=docker/dockerfile:1

################################################################################
# Create a stage for the base image.
################################################################################
FROM python:3.12 AS base

WORKDIR /app

COPY requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Remove the requirements.txt file
RUN rm /app/requirements.txt

################################################################################
# Create a stage for building/compiling the application.
################################################################################
FROM base AS development

# Copy the current directory contents into the container at /app
COPY . /app

# Installing some additional tools

ENTRYPOINT [ "python", "__main__.py" ]

################################################################################
# Create a final stage for running your application.
################################################################################
FROM base AS final

# Copy only the necessary directories and files into the container at /app
COPY src/ /app/src
COPY main.py /app/main.py
COPY locales/ /app/locales
COPY LICENSE /app/LICENSE
COPY logger.json /app/logger.json

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser

ENTRYPOINT [ "python", "main.py" ]
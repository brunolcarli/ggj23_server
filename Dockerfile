# FROM python:3.9-alpine

# RUN mkdir /app
# WORKDIR /app

# RUN apk add --no-cache \
#             --virtual \
#             .build-deps \
#             python3-dev \
#             build-base \
#             linux-headers \
#             gcc \
#             musl-dev \
#             libffi-dev \
#             openssl-dev \
#             cargo

# RUN python -m pip install --upgrade pip
# RUN python -m pip install --upgrade cython
# RUN python -m pip install --no-use-pep517 cryptography

# COPY requirements.txt .
# RUN pip install -r requirements.txt

# COPY . .

# RUN python manage.py makemigrations
# RUN	python manage.py migrate

# ENV NAME yggdrasil_server

FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install --no-install-recommends -y gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/* \
    apt-get install make \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo

RUN apt-get update && apt-get install -y python3-pip

RUN mkdir /app
WORKDIR /app

RUN python3 -m pip install --upgrade cython

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

RUN python3 manage.py makemigrations
RUN	python3 manage.py migrate


ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV NAME yggdrasil_server
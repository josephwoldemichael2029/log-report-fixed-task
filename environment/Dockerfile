FROM python:3.13-slim-bookworm@sha256:7cb7cfce1f0accc303429249ddaf2d8e4d85b5a4c4971278195ca8ec6e9dcb40

RUN pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5

WORKDIR /app

COPY access.log /app/access.log

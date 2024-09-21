FROM python:3.11-slim-buster
ARG ARKITEKT_VERSION=0.8.0

RUN pip install "arkitekt-next[all]>=${ARKITEKT_VERSION}"

RUN mkdir /app
WORKDIR /app
COPY .arkitekt_next /app/.arkitekt_next
COPY app.py /app/app.py

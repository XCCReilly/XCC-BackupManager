FROM python:3.9-slim

WORKDIR /app

ENV PORT 8080
ENV HOST 0.0.0.0

COPY . .

RUN pip install -e ".[all]" 
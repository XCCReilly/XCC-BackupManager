FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -e ".[all]" 

CMD ["/bin/bash", "-c", "uvicorn asgi:app --reload --host 0.0.0.0 --port $PORT"]
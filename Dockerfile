FROM python:3.9-slim

WORKDIR /app

RUN addgroup --gid 50001 appgroup && useradd -u 50000 -G appgroup appuser

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


COPY . .

RUN pip install -e ".[all]" 

USER appuser

CMD ["/bin/bash", "-c", "uvicorn asgi:app --reload --host 0.0.0.0 --port $PORT"]
FROM python:3.12-slim-bookworm

# System deps for psycopg
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY api/requirements.txt /app/api/requirements.txt

RUN pip install --no-cache-dir -r /app/api/requirements.txt

COPY api /app/api

EXPOSE 8000

# uvicorn runs the FastAPI app below
# ENTRYPOINT ["uvicorn"]
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

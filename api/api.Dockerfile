FROM python:3.12-slim-bookworm

# System deps for psycopg
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY . /app/api/
COPY requirements.txt .

WORKDIR /app/api

RUN pip install --no-cache-dir -r requirements.txt

# COPY . .
EXPOSE 8000

# uvicorn runs the FastAPI app below
# ENTRYPOINT ["uvicorn"]
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

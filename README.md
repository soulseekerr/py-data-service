# XVA Risk Analytics Dashboard

A production-style Python application demonstrating a modern backend/frontend architecture for financial risk analytics.

The application exposes REST APIs using **FastAPI**, consumes them from a **Streamlit** dashboard, stores data in **PostgreSQL**, and is fully containerised with **Docker Compose**.

Although inspired by XVA risk management workflows used in investment banking, the project uses simplified datasets and is intended as a software engineering portfolio project.

---

## Features

- FastAPI REST API
- Streamlit interactive dashboard
- PostgreSQL backend
- Docker Compose deployment
- Health monitoring endpoint
- Version endpoint
- Scenario Mapping viewer
- Counterparty monitoring dashboard
- Interactive AG Grid tables
- Custom JavaScript cell renderers
- Modular architecture
- Automated tests using pytest

---

## Architecture

```
                +------------------+
                |   Streamlit UI   |
                +---------+--------+
                          |
                     REST API
                          |
                +---------v--------+
                |     FastAPI      |
                +---------+--------+
                          |
                    Business Logic
                          |
                +---------v--------+
                |   PostgreSQL     |
                +------------------+
```

---

## Technology Stack

| Component | Technology |
|----------|------------|
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | PostgreSQL |
| Grid | AG Grid |
| Language | Python 3.12 |
| Containerisation | Docker Compose |
| Testing | pytest |
| HTTP | requests |
| Validation | Pydantic |

---

## Project Structure

```
project/

├── api/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── app.py
│
├── streamlit/
│   ├── api_client/
│   ├── grids/
│   ├── renderers/
│   ├── views/
│   ├── components/
│   └── app.py
│
├── db/
│
├── tests/
│
├── docker-compose.yml
└── README.md
```

---

## Example Dashboard

### Counterparty Monitoring

- Status badges
- Confidence indicators
- GRR values
- Interactive filtering
- Row selection

### Scenario Mapping

- Tier grouping
- Scenario filtering
- Mapping validation
- File monitoring

---

## Design Principles

This project intentionally separates responsibilities:

```
Streamlit View
        │
        ▼
API Client
        │
        ▼
FastAPI Router
        │
        ▼
Business Logic
        │
        ▼
Database
```

The frontend never talks directly to the database.

All communication happens through REST APIs.

---

## Running the project

```bash
docker compose up --build
```

API

```
http://localhost:8000
```

Swagger

```
http://localhost:8000/docs
```

Dashboard

```
http://localhost:8501
```

---

## Testing

Run the complete test suite

```bash
python -m pytest
```

Generate coverage

```bash
python -m pytest --cov=api --cov=streamlit --cov-report=html
```

---

## Skills Demonstrated

- Python
- FastAPI
- Streamlit
- REST APIs
- PostgreSQL
- Docker
- Docker Compose
- Pydantic
- pytest
- Software Architecture
- Dependency Separation
- Data Validation
- Error Handling
- Financial Risk Analytics

---

## Future Improvements

- Authentication
- CI/CD using GitHub Actions
- Alembic migrations
- Async database access
- Repository / Service pattern
- Ruff
- mypy
- Prometheus metrics
- OpenTelemetry

---

## About

This repository was developed as a software engineering portfolio project demonstrating modern Python application architecture inspired by front-office financial risk systems.
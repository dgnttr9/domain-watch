# Domain Watch

Domain Watch is a full-stack domain expiration tracking application. It checks domain status and expiration dates, shows failures and logs in a dashboard, supports bulk imports, exports results as CSV/JSON, and runs preset-based scheduler checks in the background.

## Architecture

```text
React + Vite + Tailwind UI
        |
        v
FastAPI backend
        |
        +--> RDAP provider
        +--> WHOIS fallback provider
        |
        v
PostgreSQL
        ^
        |
Preset scheduler worker
```

## Project Structure

```text
backend/
  app/
  migrations/
  Dockerfile
frontend/
  src/
  Dockerfile
sample-data/
docker-compose.yml
README.md
```

## Environment Variables

Copy the root example first:

```powershell
Copy-Item .env.example .env
```

Root `.env` keys:
- `DATABASE_URL`
- `API_HOST`
- `API_PORT`
- `VITE_API_BASE_URL`

Docker setup note:
- `VITE_API_BASE_URL` should point to `http://localhost:8000/api/v1` because the browser reaches the backend through the published host port, not the Docker service name.

Backend local example:
- [backend/.env.example](/Users/Acer/Desktop/domain-watch/backend/.env.example)

Frontend local example:
- [frontend/.env.example](/Users/Acer/Desktop/domain-watch/frontend/.env.example)

## Quick Start

### Full stack with Docker

```powershell
docker compose up --build
```

Services:
- `postgres` on `5432`
- `backend` on `8000`
- `frontend` on `4173`
- `worker` for preset scheduler dispatch

### Local development

Backend:

```powershell
.\dev-backend.ps1
```

Frontend:

```powershell
.\dev-frontend.ps1
```

Worker:

```powershell
.\run-worker.ps1
```

## Manual Setup

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python -m alembic upgrade head
.\.venv\Scripts\python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

## Tests

Backend:

```powershell
cd backend
.\.venv\Scripts\python -m pytest app/tests/unit app/tests/api -q
```

Frontend:

```powershell
cd frontend
npm test
npm run build
```

## Scheduler Worker

The worker uses preset-based scheduling only:
- `daily`
- `weekly`
- `monthly`

It polls due domains, runs the provider chain, stores results, and writes logs. No external queue system is used in v1.

## Export Features

Available exports:
- `CSV`
- `JSON`

Endpoints:
- `GET /api/v1/exports/domains.csv`
- `GET /api/v1/exports/domains.json`

## Import Examples

Text import example:

```text
openai.com
example.org
```

CSV import example:

```csv
domain
openai.com
example.org
```

## Release Notes

v1 includes:
- single and bulk domain entry
- txt/csv import
- domain table with recheck
- error details and logs
- preset scheduler settings
- scheduler dispatch worker
- CSV and JSON export

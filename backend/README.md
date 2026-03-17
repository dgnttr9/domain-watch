# Domain Watch Backend

FastAPI backend for domain creation, checks, imports, logs, exports, and preset-based scheduler dispatch.

## Local Run

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python -m alembic upgrade head
.\.venv\Scripts\python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Docker

The backend is containerized with:
- [backend/Dockerfile](/Users/Acer/Desktop/domain-watch/backend/Dockerfile)
- automatic `alembic upgrade head` on startup
- runtime host/port driven by environment variables

## Environment Variables

Important keys:
- `DATABASE_URL`
- `API_HOST`
- `API_PORT`
- `RAW_RESPONSE_EXCERPT_LIMIT`

See:
- [backend/.env.example](/Users/Acer/Desktop/domain-watch/backend/.env.example)

## Endpoint List

Health:
- `GET /api/v1/health`

Domains:
- `GET /api/v1/domains`
- `POST /api/v1/domains`
- `POST /api/v1/domains/check`
- `POST /api/v1/domains/{domain_id}/recheck`

Imports:
- `POST /api/v1/imports/text`
- `POST /api/v1/imports/file`

Logs:
- `GET /api/v1/logs`

Scheduler:
- `PUT /api/v1/scheduler/domains/{domain_id}`
- `POST /api/v1/scheduler/dispatch`

Exports:
- `GET /api/v1/exports/domains.csv`
- `GET /api/v1/exports/domains.json`

## Provider Architecture

Provider chain:
1. `RDAP`
2. `WHOIS fallback`

Design goals:
- modular provider adapter structure
- retry and fallback in service layer
- limited raw response excerpt storage
- provider attempt order and provider attempt details persisted for logs and diagnostics

Main files:
- [base.py](/Users/Acer/Desktop/domain-watch/backend/app/providers/base.py)
- [rdap_provider.py](/Users/Acer/Desktop/domain-watch/backend/app/providers/rdap_provider.py)
- [whois_provider.py](/Users/Acer/Desktop/domain-watch/backend/app/providers/whois_provider.py)
- [registry.py](/Users/Acer/Desktop/domain-watch/backend/app/providers/registry.py)

## Scheduler

The scheduler is preset-based in v1:
- `daily`
- `weekly`
- `monthly`

Behavior:
- domains store `scheduler_enabled`, `scheduler_preset`, and `next_check_at`
- dispatch selects due domains
- worker loop runs dispatch continuously
- no queue system is used in v1

Main files:
- [scheduler_service.py](/Users/Acer/Desktop/domain-watch/backend/app/services/scheduler_service.py)
- [scheduler_dispatch_service.py](/Users/Acer/Desktop/domain-watch/backend/app/services/scheduler_dispatch_service.py)
- [background_worker.py](/Users/Acer/Desktop/domain-watch/backend/app/scheduler/background_worker.py)

## Import / Export Flow

Import:
- text and file uploads supported
- txt and csv handled separately
- csv requires `domain` column
- validation results stored with valid/invalid counts

Export:
- current domain state can be exported as CSV or JSON

## Tests

```powershell
cd backend
.\.venv\Scripts\python -m pytest app/tests/unit app/tests/api -q
```

## Example API Usage

```powershell
curl http://127.0.0.1:8000/api/v1/health
curl -X POST http://127.0.0.1:8000/api/v1/domains -H "Content-Type: application/json" -d "{\"domain\":\"openai.com\"}"
curl -X POST http://127.0.0.1:8000/api/v1/domains/check -H "Content-Type: application/json" -d "{\"domains\":[\"openai.com\"]}"
curl -X POST http://127.0.0.1:8000/api/v1/imports/text -H "Content-Type: application/json" -d "{\"content\":\"openai.com`nexample.org\"}"
curl "http://127.0.0.1:8000/api/v1/logs?level=ERROR"
curl http://127.0.0.1:8000/api/v1/exports/domains.csv
curl -X POST "http://127.0.0.1:8000/api/v1/scheduler/dispatch?limit=25"
```

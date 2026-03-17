Set-Location $PSScriptRoot\backend
$env:APP_ENV = "development"
.\.venv\Scripts\python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

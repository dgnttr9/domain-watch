Set-Location $PSScriptRoot\backend
.\.venv\Scripts\python -c "from app.scheduler.background_worker import run_scheduler_loop; run_scheduler_loop()"

from __future__ import annotations

import time

from app.db.session import SessionLocal
from app.providers.registry import build_provider_registry
from app.services.scheduler_dispatch_service import SchedulerDispatchService


def run_scheduler_loop(poll_interval_seconds: int = 30) -> None:
    while True:
        session = SessionLocal()
        try:
            dispatcher = SchedulerDispatchService(
                session=session,
                provider_registry=build_provider_registry(),
            )
            dispatcher.dispatch_due_domains()
        finally:
            session.close()
        time.sleep(poll_interval_seconds)

from datetime import datetime, timedelta

from app.domain.enums.scheduler import SchedulerPreset


def compute_next_check_at(preset: SchedulerPreset, from_dt: datetime) -> datetime:
    if preset == SchedulerPreset.DAILY:
        return from_dt + timedelta(days=1)
    if preset == SchedulerPreset.WEEKLY:
        return from_dt + timedelta(weeks=1)
    if preset == SchedulerPreset.MONTHLY:
        return from_dt + timedelta(days=30)
    raise ValueError(f"Unsupported scheduler preset: {preset}")

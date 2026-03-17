from datetime import datetime, timezone

from app.domain.enums.scheduler import SchedulerPreset
from app.scheduler.presets import compute_next_check_at


def test_daily_preset_adds_one_day() -> None:
    now = datetime(2026, 3, 17, tzinfo=timezone.utc)
    assert compute_next_check_at(SchedulerPreset.DAILY, now).day == 18

from datetime import datetime, timezone

from app.services.domain_metrics_service import compute_days_left


def test_compute_days_left_returns_none_without_expiration() -> None:
    assert compute_days_left(None) is None


def test_compute_days_left_uses_whole_days_delta() -> None:
    now = datetime(2026, 3, 17, tzinfo=timezone.utc)
    expiration = datetime(2026, 3, 20, tzinfo=timezone.utc)
    assert compute_days_left(expiration, now) == 3

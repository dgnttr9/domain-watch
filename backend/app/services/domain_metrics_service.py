from datetime import datetime, timezone


def compute_days_left(expiration_date: datetime | None, now: datetime | None = None) -> int | None:
    if expiration_date is None:
        return None

    current = now or datetime.now(timezone.utc)
    delta = expiration_date - current
    return delta.days

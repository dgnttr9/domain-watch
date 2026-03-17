from __future__ import annotations


def truncate_excerpt(raw_text: str | None, limit: int) -> str | None:
    if not raw_text:
        return None
    if len(raw_text) <= limit:
        return raw_text
    return f"{raw_text[:limit]}..."

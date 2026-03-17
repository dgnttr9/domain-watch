import re


DOMAIN_PATTERN = re.compile(
    r"^(?=.{1,253}$)(?!-)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$",
    re.IGNORECASE,
)


def normalize_domain(value: str) -> str:
    return value.strip().lower()


def is_valid_domain(value: str) -> bool:
    normalized = normalize_domain(value)
    return bool(DOMAIN_PATTERN.fullmatch(normalized))

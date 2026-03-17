from app.core.validation import is_valid_domain, normalize_domain


def test_normalize_domain_strips_and_lowercases() -> None:
    assert normalize_domain(" Example.COM ") == "example.com"


def test_valid_domain_passes() -> None:
    assert is_valid_domain("openai.com") is True


def test_invalid_domain_fails() -> None:
    assert is_valid_domain("not a domain") is False

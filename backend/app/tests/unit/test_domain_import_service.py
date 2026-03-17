from app.services.domain_import_service import DomainImportService


def test_text_import_counts_valid_and_invalid_rows(sqlite_session) -> None:
    service = DomainImportService(session=sqlite_session)

    job = service.import_text("openai.com\nnot-a-domain\nexample.org")

    assert job.total_rows == 3
    assert job.valid_rows == 2
    assert job.invalid_rows == 1


def test_csv_import_requires_domain_column(sqlite_session) -> None:
    service = DomainImportService(session=sqlite_session)

    try:
        service.import_csv("domains.csv", b"name\nopenai.com\n")
    except Exception as exc:
        assert getattr(exc, "code", None) == "csv_domain_column_required"
    else:
        raise AssertionError("Expected validation error for missing domain column.")

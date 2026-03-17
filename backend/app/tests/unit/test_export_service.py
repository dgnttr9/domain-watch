from app.db.models import Domain
from app.services.export_service import ExportService


def test_export_service_returns_json_and_csv(sqlite_session) -> None:
    sqlite_session.add(Domain(domain="openai.com", status="pending"))
    sqlite_session.commit()

    service = ExportService(session=sqlite_session)

    json_data = service.export_domains_json()
    csv_data = service.export_domains_csv()

    assert json_data[0]["domain"] == "openai.com"
    assert "openai.com" in csv_data

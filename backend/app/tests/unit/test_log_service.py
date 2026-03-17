from app.db.models import AppLog
from app.services.log_service import LogService


def test_log_service_filters_by_domain(sqlite_session) -> None:
    sqlite_session.add(AppLog(level="INFO", scope="test", message="a", domain_id=1))
    sqlite_session.add(AppLog(level="ERROR", scope="test", message="b", domain_id=2))
    sqlite_session.commit()

    service = LogService(session=sqlite_session)
    logs = service.list_logs(domain_id=2)

    assert len(logs) == 1
    assert logs[0].message == "b"

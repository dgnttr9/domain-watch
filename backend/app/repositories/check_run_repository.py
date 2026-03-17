from sqlalchemy.orm import Session

from app.db.models import DomainCheckRun


class DomainCheckRunRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, check_run: DomainCheckRun) -> DomainCheckRun:
        self.session.add(check_run)
        return check_run

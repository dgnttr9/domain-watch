from sqlalchemy.orm import Session

from app.db.models import Domain


class SchedulerRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, domain: Domain) -> Domain:
        self.session.add(domain)
        return domain

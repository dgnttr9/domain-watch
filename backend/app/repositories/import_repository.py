from sqlalchemy.orm import Session

from app.db.models import ImportJob, ImportJobItem


class ImportRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_job(self, job: ImportJob) -> ImportJob:
        self.session.add(job)
        return job

    def add_item(self, item: ImportJobItem) -> ImportJobItem:
        self.session.add(item)
        return item

    def get_job(self, job_id: int) -> ImportJob | None:
        return self.session.get(ImportJob, job_id)

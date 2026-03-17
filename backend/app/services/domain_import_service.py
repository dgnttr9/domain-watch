from __future__ import annotations

import csv
import io

from sqlalchemy.orm import Session

from app.core.exceptions import ValidationError
from app.core.validation import is_valid_domain, normalize_domain
from app.db.models import ImportJob, ImportJobItem
from app.repositories.import_repository import ImportRepository


class DomainImportService:
    def __init__(self, *, session: Session) -> None:
        self.session = session
        self.import_repository = ImportRepository(session)

    def import_text(self, content: str) -> ImportJob:
        rows = [line.strip() for line in content.splitlines() if line.strip()]
        return self._create_import_job("txt", None, rows)

    def import_csv(self, file_name: str, content: bytes) -> ImportJob:
        decoded = content.decode("utf-8")
        reader = csv.DictReader(io.StringIO(decoded))
        if "domain" not in (reader.fieldnames or []):
            raise ValidationError("CSV must include a 'domain' column.", code="csv_domain_column_required")
        rows = [row.get("domain", "") for row in reader]
        return self._create_import_job("csv", file_name, rows)

    def _create_import_job(self, source_type: str, file_name: str | None, rows: list[str]) -> ImportJob:
        if not rows:
            raise ValidationError("Import content is empty.", code="empty_import")

        valid_rows = 0
        invalid_rows = 0
        items: list[ImportJobItem] = []

        for index, row in enumerate(rows, start=1):
            normalized = normalize_domain(row)
            is_valid = is_valid_domain(normalized)
            error_message = None if is_valid else "Invalid domain format."
            valid_rows += int(is_valid)
            invalid_rows += int(not is_valid)
            items.append(
                ImportJobItem(
                    row_number=index,
                    raw_value=row,
                    normalized_domain=normalized if is_valid else None,
                    is_valid=is_valid,
                    validation_error=error_message,
                )
            )

        job = ImportJob(
            source_type=source_type,
            file_name=file_name,
            total_rows=len(rows),
            valid_rows=valid_rows,
            invalid_rows=invalid_rows,
            status="completed",
            error_summary=None if invalid_rows == 0 else f"{invalid_rows} row(s) failed validation.",
        )

        try:
            self.import_repository.add_job(job)
            self.session.flush()
            for item in items:
                item.import_job_id = job.id
                self.import_repository.add_item(item)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

        return job

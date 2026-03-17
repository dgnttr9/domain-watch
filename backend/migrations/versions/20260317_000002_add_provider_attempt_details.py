"""Add provider attempt details to domain check runs."""

from alembic import op
import sqlalchemy as sa


revision = "20260317_000002"
down_revision = "20260317_000001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "domain_check_runs",
        sa.Column("provider_attempt_details", sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("domain_check_runs", "provider_attempt_details")

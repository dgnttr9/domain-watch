"""Initial schema."""

from alembic import op
import sqlalchemy as sa
revision = "20260317_000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "domains",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("domain", sa.String(length=253), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("provider_used", sa.String(length=32), nullable=True),
        sa.Column("expiration_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("days_left", sa.Integer(), nullable=True),
        sa.Column("last_checked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("next_check_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("scheduler_enabled", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("scheduler_type", sa.String(length=16), nullable=False, server_default="preset"),
        sa.Column("scheduler_preset", sa.String(length=16), nullable=True),
        sa.Column("scheduler_expression", sa.String(length=128), nullable=True),
        sa.Column("last_error_message", sa.Text(), nullable=True),
        sa.Column("last_error_code", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("domain"),
    )
    op.create_index("ix_domains_next_check_at", "domains", ["next_check_at"], unique=False)
    op.create_index("ix_domains_scheduler_enabled", "domains", ["scheduler_enabled"], unique=False)
    op.create_index("ix_domains_status", "domains", ["status"], unique=False)

    op.create_table(
        "import_jobs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("source_type", sa.String(length=16), nullable=False),
        sa.Column("file_name", sa.String(length=255), nullable=True),
        sa.Column("total_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("valid_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("invalid_rows", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("error_summary", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "domain_check_runs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("domain_id", sa.Integer(), nullable=False),
        sa.Column("requested_by", sa.String(length=64), nullable=True),
        sa.Column("trigger_source", sa.String(length=32), nullable=False),
        sa.Column("provider_attempt_order", sa.JSON(), nullable=True),
        sa.Column("final_provider", sa.String(length=32), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("expiration_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("days_left", sa.Integer(), nullable=True),
        sa.Column("checked_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("error_code", sa.String(length=64), nullable=True),
        sa.Column("raw_response_excerpt", sa.String(length=1000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["domain_id"], ["domains.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_domain_check_runs_checked_at", "domain_check_runs", ["checked_at"], unique=False)
    op.create_index("ix_domain_check_runs_domain_id", "domain_check_runs", ["domain_id"], unique=False)

    op.create_table(
        "app_logs",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("level", sa.String(length=16), nullable=False),
        sa.Column("scope", sa.String(length=64), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("domain_id", sa.Integer(), nullable=True),
        sa.Column("run_id", sa.Integer(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["domain_id"], ["domains.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["run_id"], ["domain_check_runs.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_app_logs_created_at", "app_logs", ["created_at"], unique=False)
    op.create_index("ix_app_logs_level", "app_logs", ["level"], unique=False)

    op.create_table(
        "import_job_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("import_job_id", sa.Integer(), nullable=False),
        sa.Column("row_number", sa.Integer(), nullable=False),
        sa.Column("raw_value", sa.Text(), nullable=False),
        sa.Column("normalized_domain", sa.String(length=253), nullable=True),
        sa.Column("is_valid", sa.Boolean(), nullable=False),
        sa.Column("validation_error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["import_job_id"], ["import_jobs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_import_job_items_import_job_id", "import_job_items", ["import_job_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_import_job_items_import_job_id", table_name="import_job_items")
    op.drop_table("import_job_items")
    op.drop_index("ix_app_logs_level", table_name="app_logs")
    op.drop_index("ix_app_logs_created_at", table_name="app_logs")
    op.drop_table("app_logs")
    op.drop_index("ix_domain_check_runs_domain_id", table_name="domain_check_runs")
    op.drop_index("ix_domain_check_runs_checked_at", table_name="domain_check_runs")
    op.drop_table("domain_check_runs")
    op.drop_table("import_jobs")
    op.drop_index("ix_domains_status", table_name="domains")
    op.drop_index("ix_domains_scheduler_enabled", table_name="domains")
    op.drop_index("ix_domains_next_check_at", table_name="domains")
    op.drop_table("domains")

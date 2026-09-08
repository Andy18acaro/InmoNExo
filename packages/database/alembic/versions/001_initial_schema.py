"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-09-08
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "districts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "district_aliases",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("district_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("districts.id"), nullable=False),
        sa.Column("alias", sa.String(160), nullable=False),
        sa.UniqueConstraint("alias", name="uq_district_aliases_alias"),
    )
    op.create_table(
        "companies",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("company_name", sa.String(255), nullable=False),
        sa.Column("website", sa.String(512), nullable=False),
        sa.Column("linkedin_url", sa.String(512)),
        sa.Column("description", sa.Text()),
        sa.Column("headquarters_location", sa.String(255)),
        sa.Column("discovered_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("last_checked_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("website", name="uq_companies_website"),
    )
    op.create_table(
        "projects",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("companies.id"), nullable=False),
        sa.Column("project_name", sa.String(255), nullable=False),
        sa.Column("project_url", sa.String(512)),
        sa.Column("district", sa.String(120)),
        sa.Column("city", sa.String(120), server_default="Lima"),
        sa.Column("region", sa.String(120), server_default="Lima"),
        sa.Column("country", sa.String(120), server_default="Peru"),
        sa.Column("address", sa.String(512)),
        sa.Column("latitude", sa.Numeric(10, 7)),
        sa.Column("longitude", sa.Numeric(10, 7)),
        sa.Column("project_status", sa.String(32), server_default="UNKNOWN"),
        sa.Column("project_type", sa.String(64)),
        sa.Column("construction_stage", sa.String(64)),
        sa.Column("launch_date", sa.DateTime(timezone=True)),
        sa.Column("delivery_date", sa.DateTime(timezone=True)),
        sa.Column("total_units", sa.Integer()),
        sa.Column("description", sa.Text()),
        sa.Column("source_url", sa.String(512), nullable=False),
        sa.Column("price_min", sa.Integer()),
        sa.Column("price_max", sa.Integer()),
        sa.Column("currency", sa.String(3)),
        sa.Column("first_seen_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("source_url", name="uq_projects_source_url"),
    )
    op.create_table(
        "units",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("projects.id"), nullable=False),
        sa.Column("unit_type", sa.String(64)),
        sa.Column("bedrooms", sa.Integer()),
        sa.Column("bathrooms", sa.Integer()),
        sa.Column("area_min_m2", sa.Numeric(8, 2)),
        sa.Column("area_max_m2", sa.Numeric(8, 2)),
        sa.Column("price_min", sa.Integer()),
        sa.Column("price_max", sa.Integer()),
        sa.Column("currency", sa.String(3)),
        sa.Column("availability", sa.String(64)),
        sa.Column("source_url", sa.String(512)),
        sa.Column("scraped_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint(
            "project_id", "unit_type", "bedrooms", "area_min_m2", name="uq_units_fingerprint"
        ),
    )
    op.create_table(
        "price_history",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("projects.id")),
        sa.Column("unit_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("units.id")),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("source_url", sa.String(512)),
    )
    op.create_table(
        "events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("event_type", sa.String(64), nullable=False),
        sa.Column("entity_type", sa.String(64), nullable=False),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("previous_value", sa.JSON()),
        sa.Column("new_value", sa.JSON()),
        sa.Column("detected_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "scrape_runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("provider_slug", sa.String(64)),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column("status", sa.String(32), server_default="running"),
        sa.Column("projects_seen", sa.Integer(), server_default="0"),
        sa.Column("projects_failed", sa.Integer(), server_default="0"),
        sa.Column("error_log", sa.Text()),
        sa.Column("apify_run_id", sa.String(128)),
        sa.Column("apify_dataset_id", sa.String(128)),
    )


def downgrade() -> None:
    op.drop_table("scrape_runs")
    op.drop_table("events")
    op.drop_table("price_history")
    op.drop_table("units")
    op.drop_table("projects")
    op.drop_table("companies")
    op.drop_table("district_aliases")
    op.drop_table("districts")

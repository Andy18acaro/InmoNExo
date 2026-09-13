from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CompanyOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company_name: str
    website: str
    linkedin_url: str | None = None
    headquarters_location: str | None = None
    discovered_at: datetime
    last_checked_at: datetime | None = None
    project_count: int = 0


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company_id: UUID
    company_name: str
    project_name: str
    project_url: str | None = None
    district: str | None = None
    city: str
    address: str | None = None
    project_status: str
    source_url: str
    price_min: int | None = None
    price_max: int | None = None
    currency: str | None = None
    first_seen_at: datetime
    last_seen_at: datetime


class MarketEventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    event_type: str
    entity_type: str
    entity_id: UUID
    previous_value: dict | None = None
    new_value: dict | None = None
    detected_at: datetime
    project_name: str | None = None
    company_name: str | None = None
    district: str | None = None
    source_url: str | None = None


class PriceSnapshotOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    project_id: UUID | None = None
    unit_id: UUID | None = None
    price: int
    currency: str
    recorded_at: datetime
    source_url: str | None = None


class OverviewOut(BaseModel):
    company_count: int
    project_count: int
    projects_with_price: int
    district_count: int
    event_count: int
    recent_event_count: int = Field(description="Events detected in the last 7 days")
    last_scrape_at: datetime | None = None
    last_scrape_status: str | None = None


class DistrictStatsOut(BaseModel):
    district: str
    project_count: int
    company_count: int
    priced_project_count: int
    min_price: int | None = None
    max_price: int | None = None
    avg_price: float | None = None

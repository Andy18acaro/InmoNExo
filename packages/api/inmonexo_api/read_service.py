import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from inmonexo_core.district import normalize_district
from inmonexo_db.models import Company, MarketEvent, Project


def list_companies(session: Session) -> list[tuple[Company, int]]:
    rows = session.execute(
        select(Company, func.count(Project.id))
        .outerjoin(Project, Project.company_id == Company.id)
        .group_by(Company.id)
        .order_by(Company.company_name)
    ).all()
    return [(company, project_count) for company, project_count in rows]


def list_projects(session: Session, district: str | None = None) -> list[Project]:
    query = select(Project).options(joinedload(Project.company)).order_by(Project.project_name)
    if district:
        canonical = normalize_district(district)
        if canonical:
            query = query.where(Project.district == canonical)
        else:
            return []
    return list(session.scalars(query).unique().all())


def get_project(session: Session, project_id: uuid.UUID) -> Project | None:
    return session.scalar(
        select(Project)
        .options(joinedload(Project.company))
        .where(Project.id == project_id)
    )


def list_events(
    session: Session,
    *,
    event_type: str | None = None,
    limit: int = 100,
) -> list[MarketEvent]:
    query = select(MarketEvent).order_by(MarketEvent.detected_at.desc()).limit(limit)
    if event_type:
        query = query.where(MarketEvent.event_type == event_type)
    return list(session.scalars(query).all())

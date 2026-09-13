import uuid

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session, joinedload

from inmonexo_core.district import normalize_district
from inmonexo_db.models import Company, MarketEvent, PriceSnapshot, Project

from inmonexo_api.schemas import MarketEventOut


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
    district: str | None = None,
    limit: int = 100,
) -> list[MarketEventOut]:
    query = (
        select(MarketEvent, Project, Company)
        .outerjoin(
            Project,
            and_(
                MarketEvent.entity_type == "project",
                MarketEvent.entity_id == Project.id,
            ),
        )
        .outerjoin(Company, Project.company_id == Company.id)
        .order_by(MarketEvent.detected_at.desc())
        .limit(limit)
    )
    if event_type:
        query = query.where(MarketEvent.event_type == event_type)
    if district:
        canonical = normalize_district(district)
        if canonical is None:
            return []
        query = query.where(Project.district == canonical)

    events: list[MarketEventOut] = []
    for event, project, company in session.execute(query).all():
        events.append(
            MarketEventOut(
                id=event.id,
                event_type=event.event_type,
                entity_type=event.entity_type,
                entity_id=event.entity_id,
                previous_value=event.previous_value,
                new_value=event.new_value,
                detected_at=event.detected_at,
                project_name=project.project_name if project is not None else None,
                company_name=company.company_name if company is not None else None,
                district=project.district if project is not None else None,
                source_url=project.source_url if project is not None else None,
            )
        )
    return events


def list_price_history(
    session: Session,
    project_id: uuid.UUID,
) -> list[PriceSnapshot]:
    return list(
        session.scalars(
            select(PriceSnapshot)
            .where(PriceSnapshot.project_id == project_id)
            .order_by(PriceSnapshot.recorded_at.asc(), PriceSnapshot.id.asc())
        ).all()
    )

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from inmonexo_api.deps import get_db
from inmonexo_api.read_service import get_project, list_price_history, list_projects
from inmonexo_api.schemas import PriceSnapshotOut, ProjectOut
from inmonexo_db.models import Project

router = APIRouter(prefix="/projects", tags=["projects"])


def project_to_schema(project: Project) -> ProjectOut:
    return ProjectOut(
        id=project.id,
        company_id=project.company_id,
        company_name=project.company.company_name,
        project_name=project.project_name,
        project_url=project.project_url,
        district=project.district,
        city=project.city,
        address=project.address,
        project_status=project.project_status,
        source_url=project.source_url,
        price_min=project.price_min,
        price_max=project.price_max,
        currency=project.currency,
        first_seen_at=project.first_seen_at,
        last_seen_at=project.last_seen_at,
    )



@router.get("", response_model=list[ProjectOut])
def get_projects(
    district: str | None = Query(default=None, description="Canonical Lima district name"),
    session: Session = Depends(get_db),
) -> list[ProjectOut]:
    return [project_to_schema(project) for project in list_projects(session, district=district)]


@router.get("/{project_id}", response_model=ProjectOut)
def get_project_by_id(
    project_id: uuid.UUID,
    session: Session = Depends(get_db),
) -> ProjectOut:
    project = get_project(session, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_to_schema(project)


@router.get("/{project_id}/price-history", response_model=list[PriceSnapshotOut])
def get_project_price_history(
    project_id: uuid.UUID,
    session: Session = Depends(get_db),
) -> list[PriceSnapshotOut]:
    project = get_project(session, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return list_price_history(session, project_id)

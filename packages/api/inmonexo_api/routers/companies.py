from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from inmonexo_api.deps import get_db
from inmonexo_api.read_service import list_companies
from inmonexo_api.schemas import CompanyOut

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("", response_model=list[CompanyOut])
def get_companies(session: Session = Depends(get_db)) -> list[CompanyOut]:
    results: list[CompanyOut] = []
    for company, project_count in list_companies(session):
        item = CompanyOut.model_validate(company)
        results.append(item.model_copy(update={"project_count": project_count}))
    return results

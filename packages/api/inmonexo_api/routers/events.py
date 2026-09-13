from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from inmonexo_api.deps import get_db
from inmonexo_api.read_service import list_events
from inmonexo_api.schemas import MarketEventOut

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[MarketEventOut])
def get_events(
    event_type: str | None = Query(default=None),
    district: str | None = Query(default=None, description="Canonical Lima district name"),
    limit: int = Query(default=100, ge=1, le=500),
    session: Session = Depends(get_db),
) -> list[MarketEventOut]:
    return list_events(session, event_type=event_type, district=district, limit=limit)

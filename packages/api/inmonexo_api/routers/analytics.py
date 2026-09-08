from dataclasses import asdict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from inmonexo_analytics.metrics import district_breakdown, overview_metrics
from inmonexo_api.deps import get_db
from inmonexo_api.schemas import DistrictStatsOut, OverviewOut

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/overview", response_model=OverviewOut)
def get_overview(session: Session = Depends(get_db)) -> OverviewOut:
    return OverviewOut(**asdict(overview_metrics(session)))


@router.get("/districts", response_model=list[DistrictStatsOut])
def get_district_stats(session: Session = Depends(get_db)) -> list[DistrictStatsOut]:
    return [DistrictStatsOut(**asdict(row)) for row in district_breakdown(session)]

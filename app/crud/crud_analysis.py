from typing import Any, List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.analysis import Analysis, AnalysisStatus
from app.schemas.analysis import AnalysisCreate, AnalysisUpdate


class CRUDAnalysis(CRUDBase[Analysis, AnalysisCreate, AnalysisUpdate]):
    def get_by_correlation_id(
        self, db: Session, *, correlation_id: str
    ) -> Optional[Analysis]:
        return (
            db.query(Analysis).filter(Analysis.correlation_id == correlation_id).first()
        )

    def get_by_website(
        self, db: Session, *, website_id: Any, skip: int = 0, limit: int = 100
    ) -> List[Analysis]:
        return (
            db.query(Analysis)
            .filter(Analysis.website_id == website_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_status(
        self,
        db: Session,
        *,
        analysis_id: Any,
        status: AnalysisStatus,
        current_stage: Optional[str] = None
    ) -> Analysis:
        analysis = self.get(db, id=analysis_id)
        update_data = {"status": status}
        if current_stage:
            update_data["current_stage"] = current_stage
        return self.update(db, db_obj=analysis, obj_in=update_data)


analysis = CRUDAnalysis(Analysis)

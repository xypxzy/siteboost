from typing import Any, List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.website import Website
from app.schemas.website import WebsiteCreate, WebsiteUpdate


class CRUDWebsite(CRUDBase[Website, WebsiteCreate, WebsiteUpdate]):
    def get_by_domain(self, db: Session, *, domain: str) -> Optional[Website]:
        return db.query(Website).filter(Website.domain == domain).first()

    def get_multi_by_user(
        self, db: Session, *, user_id: Any, skip: int = 0, limit: int = 100
    ) -> List[Website]:
        return (
            db.query(Website)
            .filter(Website.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


website = CRUDWebsite(Website)

from typing import Optional, Dict
from uuid import UUID
from pydantic import BaseModel, HttpUrl
from app.schemas.base import IDSchema


class WebsiteBase(BaseModel):
    name: str
    domain: str
    settings: Optional[Dict] = None
    analysis_defaults: Optional[Dict] = None


class WebsiteCreate(WebsiteBase):
    user_id: UUID


class WebsiteUpdate(WebsiteBase):
    name: Optional[str] = None
    domain: Optional[str] = None


class WebsiteInDBBase(WebsiteBase, IDSchema):
    user_id: UUID


class Website(WebsiteInDBBase):
    pass

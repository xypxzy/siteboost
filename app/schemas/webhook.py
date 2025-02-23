from typing import Optional, Dict, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, HttpUrl
from app.schemas.base import IDSchema


class WebhookConfigBase(BaseModel):
    url: str
    secret: str
    event_types: List[str]
    is_active: bool = True
    retry_count: int = 3
    retry_strategy: Optional[Dict] = None


class WebhookConfigCreate(WebhookConfigBase):
    website_id: UUID


class WebhookConfigUpdate(BaseModel):
    url: Optional[str] = None
    secret: Optional[str] = None
    event_types: Optional[List[str]] = None
    is_active: Optional[bool] = None
    retry_count: Optional[int] = None
    retry_strategy: Optional[Dict] = None


class WebhookConfig(WebhookConfigBase, IDSchema):
    website_id: UUID


class WebhookDeliveryBase(BaseModel):
    attempt_count: int = 0
    status: str
    request_details: Optional[Dict] = None
    response_details: Optional[Dict] = None
    next_retry_at: Optional[datetime] = None


class WebhookDeliveryCreate(WebhookDeliveryBase):
    webhook_config_id: UUID
    analysis_event_id: UUID


class WebhookDelivery(WebhookDeliveryBase, IDSchema):
    webhook_config_id: UUID
    analysis_event_id: UUID


class AnalysisEventBase(BaseModel):
    event_type: str
    event_data: Dict
    triggered_by: Optional[str] = None


class AnalysisEventCreate(AnalysisEventBase):
    analysis_id: UUID


class AnalysisEvent(AnalysisEventBase, IDSchema):
    analysis_id: UUID

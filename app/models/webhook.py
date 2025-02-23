from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy import String, JSON, ForeignKey, Boolean, Integer, DateTime
from sqlalchemy.types import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class WebhookConfig(Base):
    __tablename__ = "webhook_configs"

    website_id: Mapped[UUID] = mapped_column(ForeignKey("website.id"), nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    secret: Mapped[str] = mapped_column(String, nullable=False)
    event_types: Mapped[List[str]] = mapped_column(ARRAY(String))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=3)
    retry_strategy: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Relationships
    website: Mapped["Website"] = relationship(
        "Website", back_populates="webhook_configs"
    )
    deliveries: Mapped[List["WebhookDelivery"]] = relationship(
        "WebhookDelivery", back_populates="webhook_config"
    )


class AnalysisEvent(Base):
    __tablename__ = "analysis_events"

    analysis_id: Mapped[UUID] = mapped_column(ForeignKey("analysis.id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String, nullable=False)
    event_data: Mapped[dict] = mapped_column(JSON)
    triggered_by: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationships
    analysis: Mapped["Analysis"] = relationship("Analysis", back_populates="events")
    webhook_deliveries: Mapped[List["WebhookDelivery"]] = relationship(
        "WebhookDelivery", back_populates="analysis_event"
    )


class WebhookDelivery(Base):
    __tablename__ = "webhook_deliveries"

    webhook_config_id: Mapped[UUID] = mapped_column(
        ForeignKey("webhook_configs.id"), nullable=False
    )
    analysis_event_id: Mapped[UUID] = mapped_column(
        ForeignKey("analysis_events.id"), nullable=False
    )
    attempt_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String)
    request_details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    response_details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    next_retry_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relationships
    webhook_config: Mapped["WebhookConfig"] = relationship(
        "WebhookConfig", back_populates="deliveries"
    )
    analysis_event: Mapped["AnalysisEvent"] = relationship(
        "AnalysisEvent", back_populates="webhook_deliveries"
    )

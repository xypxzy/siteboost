from typing import List, Optional
from uuid import UUID
from sqlalchemy import String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Website(Base):
    __tablename__ = "website"

    name: Mapped[str] = mapped_column(String, nullable=False)
    domain: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    settings: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    analysis_defaults: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="website")
    analysis: Mapped[List["Analysis"]] = relationship(
        "Analysis", back_populates="website"
    )
    webhook_configs: Mapped[List["WebhookConfig"]] = relationship(
        "WebhookConfig", back_populates="website"
    )

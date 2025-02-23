from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy import String, JSON, ForeignKey, Float, Integer, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.db.base import Base


class AnalysisStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Analysis(Base):
    __tablename__ = "analysis"

    website_id: Mapped[UUID] = mapped_column(ForeignKey("website.id"), nullable=False)
    correlation_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    html_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    analysis_settings: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    status: Mapped[AnalysisStatus] = mapped_column(
        Enum(AnalysisStatus), default=AnalysisStatus.PENDING
    )
    current_stage: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    progress: Mapped[float] = mapped_column(Float, default=0.0)
    error_details: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_by: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1)

    # Relationships
    website: Mapped["Website"] = relationship("Website", back_populates="analysis")
    seo_data: Mapped["SEOData"] = relationship(
        "SEOData", back_populates="analysis", uselist=False
    )
    performance_data: Mapped["PerformanceData"] = relationship(
        "PerformanceData", back_populates="analysis", uselist=False
    )
    security_data: Mapped["SecurityData"] = relationship(
        "SecurityData", back_populates="analysis", uselist=False
    )
    accessibility_data: Mapped["AccessibilityData"] = relationship(
        "AccessibilityData", back_populates="analysis", uselist=False
    )
    recommendations: Mapped[List["Recommendation"]] = relationship(
        "Recommendation", back_populates="analysis"
    )
    events: Mapped[List["AnalysisEvent"]] = relationship(
        "AnalysisEvent", back_populates="analysis"
    )

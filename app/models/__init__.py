from app.db.base import Base
from app.models.user import User
from app.models.website import Website
from app.models.analysis import Analysis, AnalysisStatus
from app.models.analysis_data import (
    SEOData,
    PerformanceData,
    SecurityData,
    AccessibilityData,
)
from app.models.webhook import WebhookConfig, WebhookDelivery, AnalysisEvent

# For Alembic auto-generation
__all__ = [
    "Base",
    "User",
    "Website",
    "Analysis",
    "AnalysisStatus",
    "SEOData",
    "PerformanceData",
    "SecurityData",
    "AccessibilityData",
    "WebhookConfig",
    "WebhookDelivery",
    "AnalysisEvent",
]

from typing import Optional, Dict, List
from uuid import UUID
from pydantic import BaseModel, HttpUrl
from app.schemas.base import IDSchema
from app.models.analysis import AnalysisStatus


# Base Analysis Schemas
class AnalysisBase(BaseModel):
    url: str
    analysis_settings: Optional[Dict] = None
    status: AnalysisStatus = AnalysisStatus.PENDING
    current_stage: Optional[str] = None
    progress: float = 0.0
    error_details: Optional[Dict] = None
    version: int = 1


class AnalysisCreate(AnalysisBase):
    website_id: UUID
    created_by: UUID
    correlation_id: str


class AnalysisUpdate(BaseModel):
    status: Optional[AnalysisStatus] = None
    current_stage: Optional[str] = None
    progress: Optional[float] = None
    error_details: Optional[Dict] = None


class AnalysisInDBBase(AnalysisBase, IDSchema):
    website_id: UUID
    created_by: UUID
    correlation_id: str
    html_content: Optional[str] = None


class Analysis(AnalysisInDBBase):
    pass


# SEO Data Schemas
class SEODataBase(BaseModel):
    title_exists: bool = False
    title_length: Optional[int] = None
    title_content: Optional[str] = None
    description_exists: bool = False
    description_length: Optional[int] = None
    description_content: Optional[str] = None
    canonical_correct: Optional[bool] = None
    canonical_url: Optional[str] = None
    meta_tags: Optional[Dict] = None
    open_graph_data: Optional[Dict] = None
    structured_data: Optional[Dict] = None
    word_count: Optional[int] = None
    keyword_density: Optional[float] = None
    h_tags_structure: Optional[Dict] = None


class SEODataCreate(SEODataBase):
    analysis_id: UUID


class SEOData(SEODataBase, IDSchema):
    analysis_id: UUID


# Performance Data Schemas
class PerformanceDataBase(BaseModel):
    page_load_time: Optional[float] = None
    largest_contentful_paint: Optional[float] = None
    cumulative_layout_shift: Optional[float] = None
    first_input_delay: Optional[float] = None
    resource_count: Optional[int] = None
    total_page_size: Optional[float] = None
    resource_timing: Optional[Dict] = None
    network_info: Optional[Dict] = None
    time_to_interactive: Optional[float] = None
    first_contentful_paint: Optional[float] = None


class PerformanceDataCreate(PerformanceDataBase):
    analysis_id: UUID


class PerformanceData(PerformanceDataBase, IDSchema):
    analysis_id: UUID


# Security Data Schemas
class SecurityDataBase(BaseModel):
    https_enabled: bool = False
    csp_enabled: bool = False
    csp_analysis: Optional[Dict] = None
    x_frame_options_enabled: bool = False
    xss_protection_enabled: bool = False
    hsts_enabled: bool = False
    ssl_info: Optional[Dict] = None
    security_headers: Optional[Dict] = None
    vulnerability_scan: Optional[Dict] = None


class SecurityDataCreate(SecurityDataBase):
    analysis_id: UUID


class SecurityData(SecurityDataBase, IDSchema):
    analysis_id: UUID


# Accessibility Data Schemas
class AccessibilityDataBase(BaseModel):
    alt_missing_count: int = 0
    heading_structure_valid: bool = False
    contrast_ratio_avg: Optional[float] = None
    aria_violations: Optional[Dict] = None
    keyboard_navigation_issues: Optional[Dict] = None
    skip_links_present: bool = False
    color_contrast_issues: Optional[Dict] = None
    form_labels_missing: int = 0


class AccessibilityDataCreate(AccessibilityDataBase):
    analysis_id: UUID


class AccessibilityData(AccessibilityDataBase, IDSchema):
    analysis_id: UUID


# Response Schemas
class AnalysisResponse(BaseModel):
    id: UUID
    task_id: str
    correlation_id: str
    status: AnalysisStatus
    message: str


class AnalysisDetail(AnalysisInDBBase):
    seo_data: Optional[SEOData] = None
    performance_data: Optional[PerformanceData] = None
    security_data: Optional[SecurityData] = None
    accessibility_data: Optional[AccessibilityData] = None

    class Config:
        from_attributes = True


# Recommendation Schemas
class RecommendationBase(BaseModel):
    category: str
    message: str
    severity: str
    action_items: List[Dict]
    impact_score: float
    priority: int
    implementation_difficulty: str
    valid_until: Optional[str] = None


class RecommendationCreate(RecommendationBase):
    analysis_id: UUID
    generated_by: UUID


class Recommendation(RecommendationBase, IDSchema):
    analysis_id: UUID
    generated_by: UUID

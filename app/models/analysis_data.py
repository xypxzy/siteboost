from sqlalchemy import UUID, Column, ForeignKey, String, JSON, Float, Integer, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base


class SEOData(Base):
    __tablename__ = "seo_data"

    analysis_id = Column(UUID, ForeignKey("analysis.id"), nullable=False)
    title_exists = Column(Boolean, default=False)
    title_length = Column(Integer)
    title_content = Column(String)
    description_exists = Column(Boolean, default=False)
    description_length = Column(Integer)
    description_content = Column(String)
    canonical_correct = Column(Boolean)
    canonical_url = Column(String)
    meta_tags = Column(JSON)
    open_graph_data = Column(JSON)
    structured_data = Column(JSON)
    word_count = Column(Integer)
    keyword_density = Column(Float)
    h_tags_structure = Column(JSON)

    analysis = relationship("Analysis", back_populates="seo_data")


class PerformanceData(Base):
    __tablename__ = "performance_data"

    analysis_id = Column(UUID, ForeignKey("analysis.id"), nullable=False)
    page_load_time = Column(Float)
    largest_contentful_paint = Column(Float)
    cumulative_layout_shift = Column(Float)
    first_input_delay = Column(Float)
    resource_count = Column(Integer)
    total_page_size = Column(Float)
    resource_timing = Column(JSON)
    network_info = Column(JSON)
    time_to_interactive = Column(Float)
    first_contentful_paint = Column(Float)

    analysis = relationship("Analysis", back_populates="performance_data")


class SecurityData(Base):
    __tablename__ = "security_data"

    analysis_id = Column(UUID, ForeignKey("analysis.id"), nullable=False)
    https_enabled = Column(Boolean)
    csp_enabled = Column(Boolean)
    csp_analysis = Column(JSON)
    x_frame_options_enabled = Column(Boolean)
    xss_protection_enabled = Column(Boolean)
    hsts_enabled = Column(Boolean)
    ssl_info = Column(JSON)
    security_headers = Column(JSON)
    vulnerability_scan = Column(JSON)

    analysis = relationship("Analysis", back_populates="security_data")


class AccessibilityData(Base):
    __tablename__ = "accessibility_data"

    analysis_id = Column(UUID, ForeignKey("analysis.id"), nullable=False)
    alt_missing_count = Column(Integer)
    heading_structure_valid = Column(Boolean)
    contrast_ratio_avg = Column(Float)
    aria_violations = Column(JSON)
    keyboard_navigation_issues = Column(JSON)
    skip_links_present = Column(Boolean)
    color_contrast_issues = Column(JSON)
    form_labels_missing = Column(Integer)

    analysis = relationship("Analysis", back_populates="accessibility_data")

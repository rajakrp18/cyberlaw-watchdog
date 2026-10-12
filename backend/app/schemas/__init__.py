"""
Pydantic v2 request/response schemas for the LexSentry API.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field

from app.models import (
    DocumentStatus,
    DocumentType,
    LegalTopicTag,
    RelevanceScore,
    ReviewDecision,
    SourceType,
)


# ─────────────────────────────────────────────
# Source Schemas
# ─────────────────────────────────────────────

class SourceCreate(BaseModel):
    name: str
    url: str
    feed_url: Optional[str] = None
    authority_level: int = Field(default=1, ge=1, le=5)
    source_type: SourceType
    subject_area: Optional[str] = None
    check_frequency_minutes: int = Field(default=60, ge=5)
    scraper_class: Optional[str] = None
    notes: Optional[str] = None


class SourceUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    feed_url: Optional[str] = None
    authority_level: Optional[int] = None
    check_frequency_minutes: Optional[int] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None


class SourceResponse(BaseModel):
    id: uuid.UUID
    name: str
    url: str
    feed_url: Optional[str]
    authority_level: int
    source_type: SourceType
    subject_area: Optional[str]
    check_frequency_minutes: int
    is_active: bool
    last_checked_at: Optional[datetime]
    last_successful_at: Optional[datetime]
    scraper_class: Optional[str]
    notes: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────────
# Classification Schemas
# ─────────────────────────────────────────────

class ClassificationResponse(BaseModel):
    id: uuid.UUID
    tags: List[str]
    relevance_score: RelevanceScore
    confidence: Optional[float]
    reasoning: Optional[str]
    requires_lawyer_review: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────────
# Impact Note Schemas
# ─────────────────────────────────────────────

class ImpactNoteResponse(BaseModel):
    id: uuid.UUID
    what_happened: Optional[str]
    authority_detail: Optional[str]
    legal_status: Optional[str]
    what_changed: Optional[str]
    practical_relevance: Optional[str]
    caution: Optional[str]
    source_citations: Optional[List[Dict[str, Any]]]
    flagged_for_review: bool
    flag_reason: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────────
# Document Schemas
# ─────────────────────────────────────────────

class DocumentIngest(BaseModel):
    """Request body for manual ingestion."""
    url: str
    source_id: Optional[uuid.UUID] = None
    raw_text: Optional[str] = None   # If caller provides text directly


class DocumentResponse(BaseModel):
    id: uuid.UUID
    source_id: uuid.UUID
    title: str
    original_url: str
    authority: Optional[str]
    document_type: DocumentType
    publication_date: Optional[datetime]
    retrieval_date: datetime
    summary: Optional[str]
    raw_text: Optional[str] = None
    content_hash: str
    status: DocumentStatus
    version_number: int
    is_superseded: bool
    classification: Optional[ClassificationResponse] = None
    impact_note: Optional[ImpactNoteResponse] = None
    reviews: Optional[List[ReviewResponse]] = []
    created_at: datetime

    model_config = {"from_attributes": True}


class DocumentListResponse(BaseModel):
    total: int
    items: List[DocumentResponse]


# ─────────────────────────────────────────────
# Review Schemas
# ─────────────────────────────────────────────

class ReviewCreate(BaseModel):
    document_id: Optional[uuid.UUID] = None
    reviewer_name: str = "Adv. Amit Kumar Gupta (MD)"
    decision: ReviewDecision
    notes: Optional[str] = None
    matter_reference: Optional[str] = None


class ReviewResponse(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    reviewer_name: str
    decision: ReviewDecision
    notes: Optional[str] = None
    matter_reference: Optional[str] = None
    reviewed_at: datetime

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────────
# Auth Schemas
# ─────────────────────────────────────────────

class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str
    role: str = "lawyer"


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ─────────────────────────────────────────────
# Copilot / RAG Schemas
# ─────────────────────────────────────────────

class ChatMessageItem(BaseModel):
    role: str
    content: str


class CopilotQuery(BaseModel):
    question: str
    limit: int = Field(default=5, ge=1, le=20)
    history: Optional[List[ChatMessageItem]] = None


class CitationSource(BaseModel):
    document_id: str
    title: str
    authority: Optional[str]
    original_url: str
    publication_date: Optional[str]
    relevance_score: float


class CopilotResponse(BaseModel):
    answer: str
    citations: List[CitationSource]
    confidence: float
    requires_lawyer_verification: bool = True
    disclaimer: str = (
        "This response is generated by AI and must be verified by a qualified lawyer "
        "before being relied upon in any legal matter."
    )


# ─────────────────────────────────────────────
# Dashboard Stats
# ─────────────────────────────────────────────

class DashboardStats(BaseModel):
    new_developments: int
    ai_filtered: int
    pending_review: int
    action_required: int
    p0_count: int
    p1_count: int
    approved_to_kb: int

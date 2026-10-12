"""
SQLAlchemy ORM Models for LexSentry (SQLite compatible).
"""
from __future__ import annotations

import enum
import uuid
import json
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
    JSON,
    Uuid,
)
from sqlalchemy.orm import relationship

from app.database import Base

# ─────────────────────────────────────────────
# Enumerations
# ─────────────────────────────────────────────

class SourceType(str, enum.Enum):
    COURT = "COURT"
    REGULATOR = "REGULATOR"
    GAZETTE = "GAZETTE"
    MINISTRY = "MINISTRY"
    ADVISORY = "ADVISORY"

class DocumentType(str, enum.Enum):
    JUDGMENT = "JUDGMENT"
    CIRCULAR = "CIRCULAR"
    NOTIFICATION = "NOTIFICATION"
    GUIDELINE = "GUIDELINE"
    ADVISORY = "ADVISORY"
    DRAFT_RULE = "DRAFT_RULE"
    AMENDMENT = "AMENDMENT"
    PRESS_RELEASE = "PRESS_RELEASE"
    UNKNOWN = "UNKNOWN"

class DocumentStatus(str, enum.Enum):
    DISCOVERED = "DISCOVERED"         
    PROCESSING = "PROCESSING"         
    PENDING_REVIEW = "PENDING_REVIEW" 
    REVIEWED = "REVIEWED"             
    ARCHIVED = "ARCHIVED"             

class RelevanceScore(str, enum.Enum):
    P0 = "P0"  
    P1 = "P1"  
    P2 = "P2"  
    P3 = "P3"  

class ReviewDecision(str, enum.Enum):
    RELEVANT = "RELEVANT"
    NOT_RELEVANT = "NOT_RELEVANT"
    NEEDS_SENIOR_REVIEW = "NEEDS_SENIOR_REVIEW"
    APPLY_TO_MATTER = "APPLY_TO_MATTER"
    MONITOR = "MONITOR"
    APPROVED_TO_KNOWLEDGE_BASE = "APPROVED_TO_KNOWLEDGE_BASE"

class LegalTopicTag(str, enum.Enum):
    BANK_ACCOUNT_FREEZE = "BANK_ACCOUNT_FREEZE"
    LIEN = "LIEN"
    NCRP = "NCRP"
    MULE_ACCOUNT = "MULE_ACCOUNT"
    DIGITAL_FRAUD = "DIGITAL_FRAUD"
    DIGITAL_ARREST = "DIGITAL_ARREST"
    POLICE_POWERS = "POLICE_POWERS"
    JURISDICTION = "JURISDICTION"
    BANK_LIABILITY = "BANK_LIABILITY"
    VICTIM_RESTITUTION = "VICTIM_RESTITUTION"
    BNSS = "BNSS"
    BNS = "BNS"
    IT_ACT = "IT_ACT"
    DIGITAL_EVIDENCE = "DIGITAL_EVIDENCE"
    INTERMEDIARY_LIABILITY = "INTERMEDIARY_LIABILITY"
    DATA_PROTECTION = "DATA_PROTECTION"
    CYBER_SECURITY = "CYBER_SECURITY"
    OTHER = "OTHER"

# ─────────────────────────────────────────────
# Source Registry
# ─────────────────────────────────────────────
class Source(Base):
    __tablename__ = "sources"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    url = Column(Text, nullable=False)
    feed_url = Column(Text, nullable=True)        
    authority_level = Column(Integer, nullable=False, default=1)  
    source_type = Column(Enum(SourceType), nullable=False)
    subject_area = Column(String(255), nullable=True)
    check_frequency_minutes = Column(Integer, nullable=False, default=60)
    is_active = Column(Boolean, nullable=False, default=True)
    last_checked_at = Column(DateTime(timezone=True), nullable=True)
    last_successful_at = Column(DateTime(timezone=True), nullable=True)
    scraper_class = Column(String(100), nullable=True)  
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    documents = relationship("Document", back_populates="source", lazy="selectin")

# ─────────────────────────────────────────────
# Document
# ─────────────────────────────────────────────
class Document(Base):
    __tablename__ = "documents"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    source_id = Column(Uuid, ForeignKey("sources.id"), nullable=False)

    title = Column(Text, nullable=False)
    original_url = Column(Text, nullable=False)
    authority = Column(String(255), nullable=True)
    document_type = Column(Enum(DocumentType), nullable=False, default=DocumentType.UNKNOWN)
    publication_date = Column(DateTime(timezone=True), nullable=True)
    retrieval_date = Column(DateTime(timezone=True), server_default=func.now())

    raw_text = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    local_file_path = Column(Text, nullable=True)  

    content_hash = Column(String(64), nullable=False, unique=True)  

    version_number = Column(Integer, nullable=False, default=1)
    superseded_by_id = Column(Uuid, ForeignKey("documents.id"), nullable=True)
    is_superseded = Column(Boolean, nullable=False, default=False)

    status = Column(Enum(DocumentStatus), nullable=False, default=DocumentStatus.DISCOVERED)
    processing_error = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    source = relationship("Source", back_populates="documents")
    classification = relationship("Classification", back_populates="document", uselist=False, lazy="selectin")
    impact_note = relationship("ImpactNote", back_populates="document", uselist=False, lazy="selectin")
    reviews = relationship("LawyerReview", back_populates="document", lazy="selectin")
    newer_version = relationship("Document", foreign_keys=[superseded_by_id], remote_side="Document.id")

# ─────────────────────────────────────────────
# Classification
# ─────────────────────────────────────────────
class Classification(Base):
    __tablename__ = "classifications"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    document_id = Column(Uuid, ForeignKey("documents.id"), nullable=False, unique=True)

    tags_json = Column(JSON, nullable=False, default=list) # SQLite JSON
    relevance_score = Column(Enum(RelevanceScore), nullable=False, default=RelevanceScore.P3)
    confidence = Column(Float, nullable=True)  
    reasoning = Column(Text, nullable=True)    
    requires_lawyer_review = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    document = relationship("Document", back_populates="classification")

    @property
    def tags(self):
        return self.tags_json

    @tags.setter
    def tags(self, value):
        self.tags_json = value

# ─────────────────────────────────────────────
# Impact Note
# ─────────────────────────────────────────────
class ImpactNote(Base):
    __tablename__ = "impact_notes"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    document_id = Column(Uuid, ForeignKey("documents.id"), nullable=False, unique=True)

    what_happened = Column(Text, nullable=True)
    authority_detail = Column(Text, nullable=True)    
    legal_status = Column(Text, nullable=True)        
    what_changed = Column(Text, nullable=True)        
    practical_relevance = Column(Text, nullable=True) 
    caution = Column(Text, nullable=True)             
    source_citations = Column(JSON, nullable=True)    

    flagged_for_review = Column(Boolean, nullable=False, default=False)
    flag_reason = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    document = relationship("Document", back_populates="impact_note")

# ─────────────────────────────────────────────
# Lawyer Review / Audit Trail
# ─────────────────────────────────────────────
class LawyerReview(Base):
    __tablename__ = "lawyer_reviews"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    document_id = Column(Uuid, ForeignKey("documents.id"), nullable=False)

    reviewer_name = Column(String(255), nullable=False)
    decision = Column(Enum(ReviewDecision), nullable=False)
    notes = Column(Text, nullable=True)
    matter_reference = Column(String(255), nullable=True)  
    previous_decision = Column(Enum(ReviewDecision), nullable=True)  

    reviewed_at = Column(DateTime(timezone=True), server_default=func.now())

    document = relationship("Document", back_populates="reviews")

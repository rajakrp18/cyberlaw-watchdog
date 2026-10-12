"""
LangGraph state definitions and Pydantic schemas for the LLM outputs.
"""
from __future__ import annotations

import operator
from typing import Annotated, Any, Dict, List, Optional, TypedDict

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field

from app.models import LegalTopicTag, RelevanceScore


# ─── Pydantic Schemas for LLM Output ───────────────────────

class ClassificationOutput(BaseModel):
    tags: List[LegalTopicTag] = Field(
        description="List of applicable legal topic tags. Use OTHER if none apply."
    )
    relevance_score: RelevanceScore = Field(
        description="P0 (Immediate), P1 (Important), P2 (Background), or P3 (Archive)."
    )
    confidence: float = Field(
        description="Confidence score between 0.0 and 1.0", ge=0.0, le=1.0
    )
    reasoning: str = Field(
        description="Short explanation of why these tags and score were chosen."
    )
    requires_lawyer_review: bool = Field(
        description="Set to true if unsure, ambiguous, or if it relates directly to active cybercrime cases."
    )


class ImpactNoteOutput(BaseModel):
    what_happened: str = Field(description="Brief summary of what occurred.")
    authority_detail: str = Field(description="The court, regulator, or body issuing the document, and date.")
    legal_status: str = Field(description="E.g., Final judgment, interim order, circular, draft rule.")
    what_changed: str = Field(description="Does this change or clarify existing legal position?")
    practical_relevance: str = Field(description="How this specifically affects cybercrime legal matters.")
    caution: str = Field(description="Any jurisdictional, factual, statutory, or precedential limitations.")
    flagged_for_review: bool = Field(
        description="Set to true if you are guessing or hallucinating any part of this analysis."
    )
    flag_reason: Optional[str] = Field(
        description="Reason for flagging for review, if flagged_for_review is true."
    )


# ─── LangGraph State ─────────────────────────────────────────

class PipelineState(TypedDict):
    """The state dictionary passed between nodes in the LangGraph pipeline."""
    
    # Inputs
    document_id: str
    raw_text: str
    title: str
    authority: str
    document_type: str
    
    # Working memory
    messages: Annotated[List[BaseMessage], operator.add]
    
    # Outputs
    classification: Optional[ClassificationOutput]
    impact_note: Optional[ImpactNoteOutput]
    error: Optional[str]

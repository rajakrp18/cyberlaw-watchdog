"""
LangGraph workflow for processing newly ingested legal documents using Groq.
"""
from __future__ import annotations

import logging
from typing import Dict, Any

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph

from app.config import settings
from app.pipeline.state import PipelineState, ClassificationOutput, ImpactNoteOutput

logger = logging.getLogger(__name__)

# Initialize LLM with Gemini
llm = ChatGoogleGenerativeAI(
    model=settings.gemini_model,
    google_api_key=settings.gemini_api_key or "dummy",
    temperature=0.1
)

async def classify_document(state: PipelineState) -> Dict[str, Any]:
    """Node: Classifies the document and assigns relevance score."""
    logger.info(f"Classifying document {state['document_id']}")
    
    system_prompt = """You are an expert Indian Cyber Law attorney.
Your task is to classify incoming legal documents (judgments, circulars, advisories) for a law firm.
Assign relevant tags and a priority score (P0 to P3) based on the impact on cybercrime matters.
Be conservative: if unsure, require lawyer review."""

    human_prompt = f"""
Title: {state['title']}
Authority: {state['authority']}
Type: {state['document_type']}

Content (First 4000 chars):
{state['raw_text'][:4000]}
"""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]
    
    try:
        classifier = llm.with_structured_output(ClassificationOutput)
        result: ClassificationOutput = await classifier.ainvoke(messages)
        return {"classification": result}
    except Exception as e:
        logger.error(f"Classification failed: {e}")
        return {"error": str(e)}

async def generate_impact_note(state: PipelineState) -> Dict[str, Any]:
    """Node: Generates the structured impact note if relevance is high enough."""
    if state.get("error"):
        return {}

    classification = state.get("classification")
    
    # If P3 (Archive), we might skip the deep impact note generation to save tokens
    if classification and classification.relevance_score.value == "P3":
        logger.info(f"Skipping impact note for P3 document {state['document_id']}")
        return {
            "impact_note": ImpactNoteOutput(
                what_happened="Archived as low relevance.",
                authority_detail=state['authority'],
                legal_status="N/A",
                what_changed="N/A",
                practical_relevance="None.",
                caution="None.",
                flagged_for_review=False,
                flag_reason=None
            )
        }
        
    logger.info(f"Generating impact note for document {state['document_id']}")
    
    system_prompt = """You are an expert Indian Cyber Law attorney.
Generate a structured legal impact note for the provided document.
Focus strictly on cybercrime: bank account freezes, NCRP complaints, intermediary liability, etc.
Do not hallucinate. If the text is unclear, set flagged_for_review to True."""

    human_prompt = f"""
Title: {state['title']}
Content (First 8000 chars):
{state['raw_text'][:8000]}
"""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]
    
    try:
        note_generator = llm.with_structured_output(ImpactNoteOutput)
        result: ImpactNoteOutput = await note_generator.ainvoke(messages)
        return {"impact_note": result}
    except Exception as e:
        logger.error(f"Impact note generation failed: {e}")
        return {"error": str(e)}

def build_pipeline() -> StateGraph:
    """Builds the LangGraph state machine."""
    workflow = StateGraph(PipelineState)
    
    workflow.add_node("classify", classify_document)
    workflow.add_node("impact_note", generate_impact_note)
    
    workflow.set_entry_point("classify")
    workflow.add_edge("classify", "impact_note")
    workflow.add_edge("impact_note", END)
    
    return workflow.compile()

# Singleton graph instance
agent_pipeline = build_pipeline()

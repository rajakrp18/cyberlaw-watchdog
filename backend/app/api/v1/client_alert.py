import logging
import datetime
import uuid
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel

from app.database import get_db
from app.models import Document
from app.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

class AlertRequest(BaseModel):
    document_id: str

class AlertResponse(BaseModel):
    subject: str
    body: str

@router.post("/generate", response_model=AlertResponse)
async def generate_client_alert(req: AlertRequest, db: AsyncSession = Depends(get_db)):
    """Generates a professional email alert for clients based on an impact note."""
    
    # 1. Fetch document and impact note
    try:
        doc_uuid = uuid.UUID(str(req.document_id))
    except Exception:
        doc_uuid = req.document_id

    result = await db.execute(
        select(Document)
        .options(selectinload(Document.impact_note))
        .where(Document.id == doc_uuid)
    )
    doc = result.scalars().first()
    
    if not doc or not doc.impact_note:
        raise HTTPException(status_code=404, detail="Document or Impact Note not found.")

    # 2. Ask Gemini to draft the email
    system_prompt = (
        "You are Senior Partner Adv. Amit Kumar Gupta (MD) at a top-tier Indian cyber law practice. "
        "Your task is to draft an authoritative 'Urgent Client Advisory Alert' email to be sent to corporate and banking clients. "
        "Tone: Professional, urgent, highly authoritative, strategic. "
        "Structure the email cleanly in Markdown: "
        "\n1. Executive Summary & Legal Ratio"
        "\n2. Critical Operational & Legal Impacts"
        "\n3. Recommended Immediate Action Steps for In-House Counsel & Nodal Officers"
    )

    human_prompt = f"""
Document Title: {doc.title}
Authority: {doc.authority}
What Happened: {doc.impact_note.what_happened}
What Changed: {doc.impact_note.what_changed}
Practical Relevance: {doc.impact_note.practical_relevance}
Caution: {doc.impact_note.caution}
"""

    subject = f"URGENT LEGAL ADVISORY: {doc.authority} Directives on {doc.title[:55]}"
    body = None

    if settings.gemini_api_key:
        models_to_try = [settings.gemini_model, "gemini-3.5-flash-lite", "gemini-3.5-flash"]
        for mod in models_to_try:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{mod}:generateContent?key={settings.gemini_api_key}"
                payload = {
                    "contents": [{
                        "parts": [{"text": f"{system_prompt}\n\n{human_prompt}"}]
                    }],
                    "generationConfig": {
                        "temperature": 0.2,
                        "maxOutputTokens": 2048,
                    }
                }
                async with httpx.AsyncClient(timeout=20.0) as client:
                    r = await client.post(url, json=payload)
                    if r.status_code == 200:
                        data = r.json()
                        candidates = data.get("candidates", [])
                        if candidates:
                            body = candidates[0]["content"]["parts"][0]["text"]
                            break
            except Exception as ex:
                logger.warning(f"Gemini alert drafting error with {mod}: {ex}")

    # Fallback advisory if API is offline
    if not body:
        body = (
            f"### **CLIENT ADVISORY NOTE**\n\n"
            f"**TO:** Corporate & Banking In-House Legal Counsel, Compliance Officers, Nodal Heads  \n"
            f"**FROM:** Chambers of Adv. Amit Kumar Gupta (MD) — Cyber Law Practice Group  \n"
            f"**DATE:** {datetime.date.today().strftime('%d %B %Y')}  \n"
            f"**SUBJECT:** Regulatory & Judicial Directives in *{doc.title}*  \n\n"
            f"---\n\n"
            f"### 1. Executive Summary & Legal Ratio\n"
            f"{doc.impact_note.what_happened}\n\n"
            f"**Authority:** {doc.authority}  \n"
            f"**Key Shift:** {doc.impact_note.what_changed}\n\n"
            f"### 2. Critical Operational & Legal Impacts\n"
            f"• **Practical Practice Impact:** {doc.impact_note.practical_relevance}\n"
            f"• **Risk Caveat & Compliance Warning:** {doc.impact_note.caution}\n\n"
            f"### 3. Recommended Immediate Action Steps\n"
            f"1. **Audit Pending Requisitions:** Cross-verify all pending account debit freezes or incident notices against this ruling.\n"
            f"2. **Standardize Internal Playbooks:** Ensure compliance teams and Bank Nodal Officers update standard operating procedures within 48 hours.\n"
            f"3. **Consult Cyber Practice Counsel:** For matter-specific representations or Section 457 CrPC applications, contact our practice team for formal assistance."
        )

    return AlertResponse(subject=subject, body=body)

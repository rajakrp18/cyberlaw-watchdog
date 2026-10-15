import asyncio
import logging
import uuid
from datetime import datetime

from sqlalchemy.future import select

from app.database import AsyncSessionLocal
from app.models import Document, Source, DocumentStatus, DocumentType
from app.scrapers.rbi import RBIScraper
from app.scrapers.supreme_court import SupremeCourtScraper
from app.scrapers.indian_kanoon import IndianKanoonScraper
from app.scrapers.legal_news_rss import LegalNewsRSSScraper
from app.pipeline.workflow import agent_pipeline
from app.pipeline.state import PipelineState

logger = logging.getLogger(__name__)

async def get_or_create_source(session, name: str, source_type: str) -> str:
    """Gets existing source or creates a new one for our scraper."""
    result = await session.execute(select(Source).where(Source.name == name))
    source = result.scalars().first()
    if not source:
        source = Source(
            id=uuid.uuid4(),
            name=name,
            url="https://example.com",
            authority_level=1,
            source_type=source_type,
            check_frequency_minutes=60,
            is_active=True
        )
        session.add(source)
        await session.commit()
    return source.id

async def run_ingestion_cycle():
    """
    The orchestrator for Phase 4 Automation Engine.
    1. Runs the web scrapers.
    2. Filters out documents we already have.
    3. Pushes new documents through the AI pipeline (LangGraph).
    4. Saves the results to the database.
    """
    logger.info("[AUTOMATION ENGINE] Starting ingestion cycle...")

    # Initialize all scrapers — ordered from most to least reliable
    scrapers = [
        LegalNewsRSSScraper(),    # RSS feeds — most reliable, no bot blocking
        IndianKanoonScraper(),    # Public legal DB — good accessibility
        RBIScraper(),             # RBI RSS — may fail due to SSL issues
        SupremeCourtScraper(),    # SCI website — may fail due to bot blocking
    ]

    scraped_docs = []
    for scraper in scrapers:
        try:
            logger.info(f"[AUTOMATION ENGINE] Running: {scraper.source_name}")
            docs = await scraper.run()
            logger.info(f"[AUTOMATION ENGINE] {scraper.source_name}: found {len(docs)} relevant docs")
            scraped_docs.extend(docs)
        except Exception as e:
            logger.error(f"[AUTOMATION ENGINE] Scraper '{scraper.source_name}' crashed: {e}", exc_info=True)

    logger.info(f"[AUTOMATION ENGINE] Total scraped across all sources: {len(scraped_docs)} docs")
    
    # Process and save new documents
    async with AsyncSessionLocal() as session:
        for doc_data in scraped_docs:
            # Deduplication Check
            existing = await session.execute(select(Document).where(Document.content_hash == doc_data.content_hash))
            if existing.scalars().first():
                logger.info(f"Skipping duplicate: {doc_data.title}")
                continue
                
            logger.info(f"✨ New Document Found: {doc_data.title}")
            
            source_id = await get_or_create_source(session, doc_data.authority, "REGULATOR")
            
            # Step 1: Save Raw Document to Database
            new_doc = Document(
                id=uuid.uuid4(),
                source_id=source_id,
                title=doc_data.title,
                original_url=doc_data.original_url,
                authority=doc_data.authority,
                document_type=DocumentType.CIRCULAR,
                raw_text=doc_data.raw_text,
                content_hash=doc_data.content_hash,
                status=DocumentStatus.PROCESSING
            )
            session.add(new_doc)
            await session.commit()
            
            # Step 2: Push through the AI Pipeline (Phase 1)
            logger.info(f"🧠 Pushing {doc_data.title} to AI Pipeline...")
            initial_state = PipelineState(
                document_id=new_doc.id,
                title=new_doc.title,
                authority=new_doc.authority,
                document_type=new_doc.document_type.value,
                raw_text=new_doc.raw_text,
            )
            
            try:
                # Run the LangGraph workflow
                final_state = await agent_pipeline.ainvoke(initial_state)
                
                # Check results
                classification_output = final_state.get("classification")
                impact_output = final_state.get("impact_note")
                
                if classification_output and not final_state.get("error"):
                    # Here we would normally save the Classification and ImpactNote models
                    # to their respective tables (classifications, impact_notes).
                    # For MVP, we'll mark the document as successfully processed.
                    new_doc.status = DocumentStatus.AI_PROCESSED
                    new_doc.summary = f"AI Classified as {classification_output.relevance_score.value}"
                    await session.commit()
                    logger.info(f"✅ Successfully processed & classified {doc_data.title}")
                else:
                    new_doc.status = DocumentStatus.FAILED
                    new_doc.processing_error = final_state.get("error", "Unknown error")
                    await session.commit()
                    logger.error(f"❌ AI Pipeline failed for {doc_data.title}: {new_doc.processing_error}")

            except Exception as e:
                new_doc.status = DocumentStatus.FAILED
                new_doc.processing_error = str(e)
                await session.commit()
                logger.error(f"❌ AI Pipeline crashed for {doc_data.title}: {e}")
                
    logger.info("🏁 [AUTOMATION ENGINE] Ingestion cycle complete.")

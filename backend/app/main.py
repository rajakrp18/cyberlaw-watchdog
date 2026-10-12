import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.config import settings
from app.database import create_all_tables

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.pipeline.ingest import run_ingestion_cycle

async def run_scrapers_loop():
    """Background task loop that acts as the Automation Engine."""
    while True:
        logger.info("Triggering Automation Engine (Phase 4)...")
        try:
            await run_ingestion_cycle()
        except Exception as e:
            logger.error(f"Automation Engine encountered an error: {e}")
        # Wait 1 hour before scraping again
        await asyncio.sleep(3600)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting LexSentry Backend (SQLite & Groq MVP)...")
    await create_all_tables()
    
    # Start background tasks
    task = asyncio.create_task(run_scrapers_loop())
    
    yield
    # Shutdown
    logger.info("Shutting down LexSentry Backend...")
    task.cancel()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan
)

# CORS
if settings.get_cors_origins():
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.get_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok", "app": settings.app_name}

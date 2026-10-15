import asyncio
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.v1 import api_router
from app.config import settings
from app.database import create_all_tables

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.pipeline.ingest import run_ingestion_cycle

# ─── Resolve frontend static files path ──────────────────────────────────────
# When running as a PyInstaller exe, files are extracted to sys._MEIPASS.
# In development, they live in the normal project tree.
if getattr(sys, 'frozen', False):
    # Running inside a PyInstaller exe
    _base = Path(sys._MEIPASS)
else:
    # Running normally (dev mode)
    _base = Path(__file__).resolve().parent.parent.parent  # backend/app/main.py -> project root

FRONTEND_OUT = _base / "frontend" / "out"
logger.info(f"Frontend static path: {FRONTEND_OUT} (exists={FRONTEND_OUT.exists()})")

async def run_scrapers_loop():
    """Background task loop that acts as the Automation Engine."""
    await asyncio.sleep(30)  # Let server start and serve requests first
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

# ─── Serve Next.js static export ─────────────────────────────────────────────
# Mount AFTER API routes so /api/v1/* takes priority
if FRONTEND_OUT.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_OUT), html=True), name="frontend")
    logger.info("Frontend static files mounted at /")
else:
    # Catch-all fallback when no frontend is built yet
    @app.get("/{full_path:path}")
    def frontend_fallback(full_path: str):
        return {"message": "Frontend not built. Run: cd frontend && npm run build"}

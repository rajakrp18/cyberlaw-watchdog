from fastapi import APIRouter

from . import documents, sources, dashboard, copilot, client_alert, config

api_router = APIRouter()

api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(sources.router, prefix="/sources", tags=["Sources"])
api_router.include_router(documents.router, prefix="/documents", tags=["Documents"])
api_router.include_router(copilot.router, prefix="/copilot", tags=["Copilot"])
api_router.include_router(client_alert.router, prefix="/alert", tags=["Client Alert"])
api_router.include_router(config.router, prefix="/config", tags=["Configuration"])

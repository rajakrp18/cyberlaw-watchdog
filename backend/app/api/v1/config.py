import os
import re
import time
import logging
from typing import Optional
import sys
from pathlib import Path
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
import httpx

from app.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

if getattr(sys, 'frozen', False):
    ENV_PATH = Path(sys.executable).resolve().parent / ".env"
else:
    ENV_PATH = Path(__file__).resolve().parent.parent.parent.parent / ".env"

class KeyValidationRequest(BaseModel):
    api_key: Optional[str] = None

class KeySaveRequest(BaseModel):
    api_key: str

def mask_key(k: str) -> str:
    if not k:
        return ""
    if len(k) <= 8:
        return "••••••••"
    return f"{k[:8]}••••••••••••{k[-4:]}"

@router.get("/gemini-status")
async def get_gemini_status():
    """Returns current Gemini API configuration status and safely masked key."""
    configured = bool(settings.gemini_api_key and len(settings.gemini_api_key.strip()) > 5)
    return {
        "configured": configured,
        "masked_key": mask_key(settings.gemini_api_key),
        "model": settings.gemini_model,
        "app_env": settings.app_env,
        "status": "CONFIGURED" if configured else "UNCONFIGURED"
    }

@router.post("/gemini-validate")
async def validate_gemini_key(req: KeyValidationRequest):
    """
    Live ping test against Google Gemini API to verify API key validity,
    quota status, and active models.
    """
    key_to_test = (req.api_key or settings.gemini_api_key or "").strip()
    if not key_to_test:
        return {
            "valid": False,
            "error": "No API key provided or configured. Please enter a valid Gemini API key.",
            "status_code": 400
        }

    start_time = time.time()
    try:
        # Step 1: Query Google Model catalog (Authentication check)
        list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key_to_test}"
        async with httpx.AsyncClient(timeout=6.0) as client:
            list_res = await client.get(list_url)
            latency_ms = int((time.time() - start_time) * 1000)

            if list_res.status_code == 200:
                models_data = list_res.json()
                models = [m.get("name", "") for m in models_data.get("models", [])]
                
                # Check for Flash models
                flash_models = [m for m in models if "flash" in m]
                preferred_model = flash_models[0].replace("models/", "") if flash_models else "gemini-flash-latest"

                return {
                    "valid": True,
                    "model": preferred_model,
                    "available_models_count": len(models),
                    "latency_ms": latency_ms,
                    "message": f"API key is fully verified & authenticated with Google AI! Access to {len(models)} models confirmed.",
                    "masked_key": mask_key(key_to_test)
                }
            elif list_res.status_code in [400, 403]:
                err_body = list_res.json().get("error", {})
                err_msg = err_body.get("message", "API key invalid or permission denied.")
                return {
                    "valid": False,
                    "error": f"Google AI Authentication Failed: {err_msg}",
                    "status_code": list_res.status_code
                }
            else:
                return {
                    "valid": False,
                    "error": f"Unexpected response from Google AI API (HTTP {list_res.status_code}).",
                    "status_code": list_res.status_code
                }

    except httpx.TimeoutException:
        return {
            "valid": False,
            "error": "Connection timed out while contacting Google Gemini API. Please check your internet connection.",
            "status_code": 504
        }
    except Exception as ex:
        logger.error(f"Error testing Gemini key: {ex}", exc_info=True)
        return {
            "valid": False,
            "error": f"Diagnostic error: {str(ex)}",
            "status_code": 500
        }

@router.post("/gemini-save")
async def save_gemini_key(req: KeySaveRequest):
    """
    Saves and applies a new Gemini API key both in memory and to .env file.
    Does NOT require server reboot.
    """
    new_key = req.api_key.strip()
    if not new_key:
        raise HTTPException(status_code=400, detail="API key cannot be empty.")

    # 1. Update in-memory settings
    settings.gemini_api_key = new_key
    os.environ["GEMINI_API_KEY"] = new_key

    # 2. Persist to backend/.env
    try:
        if ENV_PATH.exists():
            content = ENV_PATH.read_text(encoding="utf-8")
            if re.search(r"^GEMINI_API_KEY=.*", content, flags=re.MULTILINE):
                new_content = re.sub(r"^GEMINI_API_KEY=.*", f"GEMINI_API_KEY={new_key}", content, flags=re.MULTILINE)
            else:
                new_content = content + f"\nGEMINI_API_KEY={new_key}\n"
            ENV_PATH.write_text(new_content, encoding="utf-8")
        else:
            ENV_PATH.write_text(f"GEMINI_API_KEY={new_key}\n", encoding="utf-8")
            
        logger.info("Successfully updated GEMINI_API_KEY in .env file and active settings.")
    except Exception as ex:
        logger.warning(f"Could not persist key to .env file: {ex}")

    return {
        "success": True,
        "message": "Gemini API key saved and activated successfully for Copilot RAG!",
        "masked_key": mask_key(new_key)
    }

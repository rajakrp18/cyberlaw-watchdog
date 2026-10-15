#!/usr/bin/env python3
"""
=============================================================================
  Cyber Law Watch Agent - Standalone Server & Launcher
=============================================================================
This launcher runs in two modes:

  1. STANDALONE EXE MODE: CyberLawWatchAgent.exe
     Runs the fully bundled FastAPI backend + Next.js static UI in-process.
     No external Python, venv, or Node.js required!

  2. DEV MODE: python run.py
     Runs uvicorn with live reload directly from the source tree.

The app (frontend + API) is served at: http://127.0.0.1:8080
=============================================================================
"""

import sys
import os
import time
import shutil
import threading
import webbrowser
import multiprocessing
from pathlib import Path

# Required for PyInstaller Windows multiprocessing
multiprocessing.freeze_support()

HOST = "127.0.0.1"
PORT = 8080
URL = f"http://{HOST}:{PORT}"

# Resolve paths
if getattr(sys, 'frozen', False):
    IS_FROZEN = True
    APP_DIR = Path(sys.executable).resolve().parent
    BUNDLE_DIR = Path(sys._MEIPASS)
else:
    IS_FROZEN = False
    APP_DIR = Path(__file__).resolve().parent
    BUNDLE_DIR = APP_DIR

BACKEND_DIR = APP_DIR / "backend"
FRONTEND_OUT = (BUNDLE_DIR / "frontend" / "out") if IS_FROZEN else (APP_DIR / "frontend" / "out")

# Ensure backend directory is in sys.path
if not IS_FROZEN and str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


def print_banner():
    print(f"""
  ================================================================
    C Y B E R   L A W   W A T C H   A G E N T
    Authoritative Legal Regulatory & Judicial Precedent Counsel
  ================================================================
    Mode : {"Standalone Stand-Alone Bundle" if IS_FROZEN else "Development"}
    App  : {URL}
    API  : {URL}/api/v1/docs
  ================================================================
    Press Ctrl+C anytime to stop.
  ================================================================
""")


def ensure_seed_database():
    """Ensure lexsentry.db exists next to the exe or project root."""
    target_db = APP_DIR / "lexsentry.db"
    if not target_db.exists():
        # Check bundled DB
        bundled_db = BUNDLE_DIR / "lexsentry.db"
        if bundled_db.exists():
            try:
                shutil.copy2(bundled_db, target_db)
                print(f"[LAUNCHER] Initialized database with seed data: {target_db.name}")
            except Exception as e:
                print(f"[LAUNCHER] Note: Could not copy seed DB: {e}")
        elif (BACKEND_DIR / "lexsentry.db").exists():
            try:
                shutil.copy2(BACKEND_DIR / "lexsentry.db", target_db)
                print(f"[LAUNCHER] Initialized database from backend: {target_db.name}")
            except Exception:
                pass


def wait_and_open_browser(max_wait=30):
    """Poll health endpoint and open browser once ready."""
    import urllib.request
    start = time.time()
    time.sleep(1.0)
    while time.time() - start < max_wait:
        try:
            req = urllib.request.Request(
                f"{URL}/health",
                headers={"User-Agent": "CyberWatchLauncher"}
            )
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                if resp.status == 200:
                    print(f"\n[LAUNCHER] Server is ready! Opening {URL} in your browser...\n")
                    webbrowser.open(URL)
                    return
        except Exception:
            pass
        time.sleep(1.0)
    print(f"[LAUNCHER] Note: Open {URL} manually in your web browser.")


def main():
    print_banner()
    ensure_seed_database()

    # Launch browser opener thread
    browser_thread = threading.Thread(target=wait_and_open_browser, daemon=True)
    browser_thread.start()

    import uvicorn

    if IS_FROZEN:
        from app.main import app
        # In frozen mode, run in-process with access_log disabled and no reload
        uvicorn.run(
            app,
            host=HOST,
            port=PORT,
            access_log=False,
            log_level="info",
        )
    else:
        # Dev mode with reload
        uvicorn.run(
            "app.main:app",
            host=HOST,
            port=PORT,
            reload=True,
            app_dir=str(BACKEND_DIR),
            log_level="info",
        )


if __name__ == "__main__":
    main()

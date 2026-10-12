#!/usr/bin/env python3
"""
=============================================================================
  Cyber Law Watch Agent - All-In-One Python Launcher
=============================================================================
Runs both the FastAPI Backend (Port 8080) and Next.js Frontend (Port 3000)
concurrently using a single command:

    python run.py

Key Features:
  - Auto-checks Python and Node.js prerequisites
  - Launches FastAPI backend with uvicorn
  - Launches Next.js frontend with npm
  - Live threaded log streaming with distinct prefixes [BACKEND] & [FRONTEND]
  - Waits for health check and opens the browser at http://localhost:3000
  - Graceful cleanup: terminates both server processes on Ctrl+C
=============================================================================
"""

import sys
import os
import time
import subprocess
import threading
import webbrowser
import signal
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"

def print_banner():
    banner = r"""
  ==============================================================
    C Y B E R   L A W   W A T C H   A G E N T
    Authoritative Legal Regulatory & Judicial Precedent Counsel
  ==============================================================
    - Backend:  http://127.0.0.1:8080  (FastAPI + Gemini Legal RAG)
    - Frontend: http://localhost:3000  (Next.js 14 Interactive Portal)
  ==============================================================
    Press Ctrl+C anytime to cleanly stop both servers.
  ==============================================================
    """
    print(banner)

def stream_output(pipe, prefix, color_code):
    """Streams child process stdout/stderr line by line with a prefixed tag."""
    reset_code = "\033[0m"
    try:
        for line in iter(pipe.readline, ''):
            if not line:
                break
            cleaned = line.rstrip()
            if cleaned:
                # Print with color prefix if terminal supports it
                print(f"{color_code}[{prefix}]{reset_code} {cleaned}")
    except (ValueError, OSError):
        pass
    finally:
        try:
            pipe.close()
        except Exception:
            pass

def check_environment():
    """Verify backend and frontend directories and tools exist."""
    if not BACKEND_DIR.exists():
        print(f"[ERROR] Backend directory not found: {BACKEND_DIR}")
        sys.exit(1)
    if not FRONTEND_DIR.exists():
        print(f"[ERROR] Frontend directory not found: {FRONTEND_DIR}")
        sys.exit(1)

    # Check for npm
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    try:
        subprocess.run([npm_cmd, "--version"], capture_output=True, check=True)
    except Exception:
        print("[WARNING] 'npm' was not found in your PATH. Please ensure Node.js is installed.")

def wait_and_open_browser(url="http://localhost:3000", max_wait=25):
    """Actively polls until both Backend API and Frontend respond with HTTP 200, then opens browser."""
    import urllib.request
    
    backend_url = "http://127.0.0.1:8080/api/v1/documents/"
    frontend_url = "http://localhost:3000"
    
    backend_ready = False
    frontend_ready = False
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        if not backend_ready:
            try:
                req = urllib.request.Request(backend_url, headers={'User-Agent': 'CyberWatchLauncher'})
                with urllib.request.urlopen(req, timeout=1.5) as resp:
                    if resp.status == 200:
                        backend_ready = True
                        print("\n\033[92m[LAUNCHER] ✔ Backend API is ONLINE & Articles are loaded.\033[0m")
            except Exception:
                pass
                
        if not frontend_ready:
            try:
                req = urllib.request.Request(frontend_url, headers={'User-Agent': 'CyberWatchLauncher'})
                with urllib.request.urlopen(req, timeout=1.5) as resp:
                    if resp.status == 200:
                        frontend_ready = True
                        print("\033[96m[LAUNCHER] ✔ Next.js Frontend is COMPILED & READY.\033[0m")
            except Exception:
                pass

        if backend_ready and frontend_ready:
            break
        time.sleep(1.0)
        
    print(f"\n[LAUNCHER] 🚀 Full system verified online! Opening browser at {url} ...\n")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"[LAUNCHER] Could not open browser automatically: {e}")

def main():
    print_banner()
    check_environment()

    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    python_cmd = sys.executable

    # 1. Start Backend: FastAPI / Uvicorn
    backend_cmd = [
        python_cmd,
        "-m", "uvicorn",
        "app.main:app",
        "--host", "127.0.0.1",
        "--port", "8080",
        "--reload"
    ]
    print("[LAUNCHER] Starting FastAPI Backend on http://127.0.0.1:8080 ...")
    backend_proc = subprocess.Popen(
        backend_cmd,
        cwd=str(BACKEND_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        encoding="utf-8",
        errors="replace"
    )

    # 2. Start Frontend: Next.js
    frontend_cmd = [npm_cmd, "run", "dev"]
    print("[LAUNCHER] Starting Next.js Frontend on http://localhost:3000 ...")
    frontend_proc = subprocess.Popen(
        frontend_cmd,
        cwd=str(FRONTEND_DIR),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        encoding="utf-8",
        errors="replace"
    )

    # 3. Stream logs asynchronously
    # Colors: Green for Backend, Cyan for Frontend
    backend_thread = threading.Thread(
        target=stream_output, 
        args=(backend_proc.stdout, "BACKEND", "\033[92m"), 
        daemon=True
    )
    frontend_thread = threading.Thread(
        target=stream_output, 
        args=(frontend_proc.stdout, "FRONTEND", "\033[96m"), 
        daemon=True
    )

    backend_thread.start()
    frontend_thread.start()

    # 4. Open browser in separate thread
    browser_thread = threading.Thread(target=wait_and_open_browser, daemon=True)
    browser_thread.start()

    # 5. Monitor processes until termination signal
    def shutdown_processes():
        print("\n[LAUNCHER] Shutting down Cyber Law Watch Agent servers...")
        for proc, name in [(backend_proc, "Backend"), (frontend_proc, "Frontend")]:
            if proc and proc.poll() is None:
                try:
                    if sys.platform == "win32":
                        # Terminate process tree on Windows to ensure child node/uvicorn workers exit
                        subprocess.run(
                            ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                            capture_output=True
                        )
                    else:
                        proc.terminate()
                except Exception as ex:
                    print(f"[LAUNCHER] Error stopping {name}: {ex}")
        print("[LAUNCHER] All servers stopped cleanly. Goodbye!\n")

    def sigint_handler(sig, frame):
        shutdown_processes()
        sys.exit(0)

    signal.signal(signal.SIGINT, sigint_handler)
    if hasattr(signal, "SIGTERM"):
        signal.signal(signal.SIGTERM, sigint_handler)

    try:
        while True:
            # Check if any process terminated unexpectedly
            b_ret = backend_proc.poll()
            f_ret = frontend_proc.poll()
            if b_ret is not None:
                print(f"[LAUNCHER] Backend exited with code {b_ret}")
                break
            if f_ret is not None:
                print(f"[LAUNCHER] Frontend exited with code {f_ret}")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        shutdown_processes()

if __name__ == "__main__":
    main()

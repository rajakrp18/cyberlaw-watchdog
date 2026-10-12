@echo off
TITLE Cyber Law Watch Agent - Unified Launcher
COLOR 0B

echo ===============================================================================
echo                 CYBER LAW WATCH AGENT - UNIFIED LAUNCHER
echo          Authoritative Indian Cyber Jurisprudence ^& Practice Intelligence
echo ===============================================================================
echo.

:: Get root directory of project
set ROOT_DIR=%~dp0
cd /d "%ROOT_DIR%"

echo [1/3] Starting FastAPI Backend (Port 8080)...
start "Cyber Law Watch Backend (Port 8080)" cmd /k "cd /d %ROOT_DIR%backend && .\venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload"

echo [2/3] Starting Next.js Frontend (Port 3000)...
start "Cyber Law Watch Frontend (Port 3000)" cmd /k "cd /d %ROOT_DIR%frontend && npm run dev"

echo [3/3] Waiting for servers to initialize...
timeout /t 4 /nobreak >nul

echo Opening Cyber Law Watch Agent in your browser...
start http://localhost:3000

echo.
echo ===============================================================================
echo   SERVICES ARE RUNNING:
echo   - Frontend: http://localhost:3000
echo   - Backend:  http://127.0.0.1:8080
echo   - API Docs: http://127.0.0.1:8080/docs
echo.
echo   To shut down, simply close the two opened terminal windows.
echo ===============================================================================
pause

# Cyber Law Watch Agent - Unified PowerShell Launcher
# Runs both FastAPI Backend and Next.js Frontend concurrently

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "          CYBER LAW WATCH AGENT - POWERSHELL LAUNCHER            " -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/3] Starting FastAPI Backend on http://127.0.0.1:8080..." -ForegroundColor Yellow
$backendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$scriptPath\backend'; .\venv\Scripts\python -m uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload" -PassThru

Write-Host "[2/3] Starting Next.js Frontend on http://localhost:3000..." -ForegroundColor Yellow
$frontendProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "Set-Location '$scriptPath\frontend'; npm run dev" -PassThru

Start-Sleep -Seconds 3

Write-Host "[3/3] Opening dashboard in default browser..." -ForegroundColor Green
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "=================================================================" -ForegroundColor Green
Write-Host "  SERVICES RUNNING CONCURRENTLY:" -ForegroundColor Green
Write-Host "  * Frontend UI:   http://localhost:3000" -ForegroundColor White
Write-Host "  * REST API:      http://127.0.0.1:8080" -ForegroundColor White
Write-Host "  * Swagger Docs:  http://127.0.0.1:8080/docs" -ForegroundColor White
Write-Host "=================================================================" -ForegroundColor Green
Write-Host "To stop services, close the individual PowerShell windows." -ForegroundColor Gray

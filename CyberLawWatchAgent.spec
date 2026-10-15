# -*- mode: python ; coding: utf-8 -*-
#
# CyberLawWatchAgent.spec
#
# Standalone Single-File Executable Specification
# Bundles:
#   - Python runtime & standard libraries
#   - FastAPI, Uvicorn, SQLAlchemy (asyncio/sqlite), LangChain, Google GenAI
#   - Next.js compiled frontend (frontend/out)
#   - Pre-populated SQLite legal database (lexsentry.db)
#
# Users can run this single .exe on Windows with ZERO external dependencies!

from pathlib import Path

ROOT = Path(SPECPATH)
BACKEND_DIR = ROOT / 'backend'
FRONTEND_OUT = ROOT / 'frontend' / 'out'
DB_FILE = BACKEND_DIR / 'lexsentry.db'

datas = [
    (str(FRONTEND_OUT), 'frontend/out'),
]

if DB_FILE.exists():
    datas.append((str(DB_FILE), '.'))

hiddenimports = [
    'uvicorn',
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespans',
    'uvicorn.lifespans.on',
    'uvicorn.lifespans.off',
    'aiosqlite',
    'sqlite3',
    'fastapi',
    'fastapi.middleware.cors',
    'fastapi.staticfiles',
    'starlette.middleware',
    'starlette.middleware.cors',
    'starlette.staticfiles',
    'starlette.responses',
    'pydantic',
    'pydantic_settings',
    'sqlalchemy',
    'sqlalchemy.ext.asyncio',
    'sqlalchemy.dialects.sqlite',
    'sqlalchemy.dialects.sqlite.aiosqlite',
    'langchain',
    'langchain_core',
    'langchain_google_genai',
    'google.genai',
    'google.auth',
    'feedparser',
    'feedparser_sgmllib',
    'bs4',
    'httpx',
    'httpcore',
    'certifi',
    'email_validator',
    'reportlab',
    'reportlab.platypus',
    'reportlab.lib',
    'reportlab.lib.colors',
    'reportlab.lib.pagesizes',
    'reportlab.lib.styles',
    'app',
    'app.main',
    'app.config',
    'app.database',
    'app.models',
    'app.schemas',
    'app.api.v1',
    'app.pipeline',
    'app.pipeline.workflow',
    'app.pipeline.ingest',
    'app.scrapers',
]

a = Analysis(
    [str(ROOT / 'run.py')],
    pathex=[str(ROOT), str(BACKEND_DIR)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['playwright', 'tkinter', 'matplotlib', 'PIL.ImageTk'],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CyberLawWatchAgent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,           # Keep console visible so user sees startup progress and logs
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

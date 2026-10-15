# 🛡️ Cyber Law Watch Agent — Tester Setup Guide

> **Version**: Beta Testing Build  
> **Platform**: Windows 10 / 11 (64-bit)  
> **Contact**: Share feedback with the development team after testing.

---

## 📋 What You're Testing

The **Cyber Law Watch Agent** is an AI-powered legal intelligence tool that:
- Monitors authoritative Indian cyber law sources (Supreme Court, High Courts, RBI, CERT-In, MHA/I4C)
- Classifies rulings by priority (P0 Critical / P1 High / P2 Info)
- Maps case law to active client matters
- Provides an AI Legal Co-Pilot (powered by Gemini) for natural language queries

---

## ✅ Prerequisites

### 1. Python 3.11 or higher (Required)

> [!IMPORTANT]
> Python is the **only** software you need to install. Node.js is NOT required.

**Check if you already have Python:**
```powershell
python --version
```
If it shows `Python 3.11.x` or higher → you're good. Skip to Step 2.

**If not installed:**
1. Download from [python.org/downloads](https://www.python.org/downloads/)
2. Run the installer
3. ✅ **Check "Add Python to PATH"** during installation (critical!)
4. Click **Install Now**

**Verify installation:**
```powershell
python --version
pip --version
```
Both should return version numbers.

---

## 📁 One-Time Setup

### Step 1 — Extract the ZIP

Extract the provided `CyberLawWatchAgent.zip` anywhere on your computer.  
Example: `C:\Users\YourName\Desktop\cyber_watch_agent\`

You should see this structure:
```
cyber_watch_agent/
├── dist/
│   └── CyberLawWatchAgent.exe   ← the launcher
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── .env                     ← API key config (see Step 3)
└── frontend/
    └── out/                     ← pre-built UI (no setup needed)
```

### Step 2 — Install Python Dependencies

Open **PowerShell** or **Command Prompt** inside the extracted folder and run:

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

> [!NOTE]
> This downloads ~500MB of AI/legal packages (langchain, fastapi, etc.).  
> It only needs to be done **once**. Grab a coffee ☕

Expected final output:
```
Successfully installed fastapi uvicorn langchain ... (many packages)
```

### Step 3 — Configure the API Key

The AI Co-Pilot requires a **Google Gemini API Key**.

1. Open `backend\.env` in any text editor (Notepad works)
2. Find the line: `GEMINI_API_KEY=`
3. Paste your key after the `=` sign:
   ```
   GEMINI_API_KEY=AIzaSy...yourkey...here
   ```
4. Save the file

> [!TIP]
> Don't have a key? Get a free one at [aistudio.google.com](https://aistudio.google.com/app/apikey)  
> Alternatively, the app works without a key — only the AI Co-Pilot tab will be disabled.

---

## 🚀 Running the App

### Double-click method
Navigate to `dist\` and **double-click `CyberLawWatchAgent.exe`**

### Or from PowerShell:
```powershell
.\dist\CyberLawWatchAgent.exe
```

### What you'll see:

```
  ================================================================
    C Y B E R   L A W   W A T C H   A G E N T
    Authoritative Legal Regulatory & Judicial Precedent Counsel
  ================================================================
    App : http://127.0.0.1:8080
    API : http://127.0.0.1:8080/api/v1/docs
  ================================================================

[LAUNCHER] Python  : C:\...\backend\venv\Scripts\python.exe
[LAUNCHER] Starting server on http://127.0.0.1:8080 ...

✔ Server ONLINE — opening http://127.0.0.1:8080
```

The browser will **open automatically** in 5–15 seconds.  
If it doesn't, manually go to: **http://127.0.0.1:8080**

> [!NOTE]
> The first startup may take 30–60 seconds while the database initializes and the AI pipeline loads. Subsequent startups are faster.

---

## 🖥️ Using the App

| Section | What to test |
|---|---|
| **Dashboard** | Legal rulings feed — check P0/P1/P2 priorities load |
| **Search & Filter** | Try filtering by authority (Supreme Court, RBI) and date range |
| **Document Viewer** | Click any ruling to open the full text + PDF viewer |
| **Matter Matching** | Check if rulings map correctly to the active client matters panel |
| **Lawyer Review** | Submit a review decision on a document |
| **AI Co-Pilot** | Ask a legal question, e.g. *"What are the latest bank freeze rulings?"* |
| **API Key Config** | Use the 🔑 button in the header to validate/update the Gemini key |
| **Refresh Feed** | Click "Refresh Feed" to trigger a live scrape from authoritative sources |

---

## 🛑 Stopping the App

Press **`Ctrl + C`** in the console window, or simply **close** the console window.

```
[LAUNCHER] Stopping server...
[LAUNCHER] Goodbye!
```

---

## 🔧 Troubleshooting

### ❌ "Backend directory not found"
The `.exe` must stay inside the `dist\` folder within the project.  
Do **not** move the `.exe` out of the extracted ZIP structure.

### ❌ "Virtual environment not found"
You haven't run Step 2 yet. Open PowerShell in the project root and run:
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### ❌ Browser opens but shows a blank page or "Frontend not built"
The static UI files are missing. Run:
```powershell
cd frontend
npm install
npm run build
```
*(This requires Node.js — contact the dev team if you hit this.)*

### ❌ AI Co-Pilot says "Error connecting to backend"
Check that your `GEMINI_API_KEY` is correctly set in `backend\.env`.  
Click the 🔑 **API Key Config** button in the app header to validate it live.

### ❌ Port 8080 already in use
Another process is using port 8080. Find and stop it:
```powershell
netstat -ano | findstr :8080
taskkill /PID <PID_NUMBER> /F
```
Then relaunch the exe.

### ❌ Antivirus blocks the EXE
Some antivirus software flags PyInstaller exes as suspicious (false positive).  
Add `CyberLawWatchAgent.exe` to your antivirus exclusion list, or run from PowerShell directly.

---

## 📬 Reporting Issues

When reporting a bug, please include:
1. **What you did** (steps to reproduce)
2. **What you expected** to happen
3. **What actually happened** (error message / screenshot)
4. **Console output** — copy the text from the black launcher window

---

*Cyber Law Watch Agent — Beta Testing Build • Confidential*

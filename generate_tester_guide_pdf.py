# -*- coding: utf-8 -*-
"""
Generate a professional PDF tester guide for Cyber Law Watch Agent.
Run with: backend\\venv\\Scripts\\python.exe generate_tester_guide_pdf.py
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import ListFlowable, ListItem
from datetime import date

OUTPUT = "TESTER_GUIDE.pdf"

# ─── Colour palette ───────────────────────────────────────────────────────────
NAVY        = colors.HexColor("#1e3a5f")
BLUE        = colors.HexColor("#2563eb")
LIGHT_BLUE  = colors.HexColor("#dbeafe")
TEAL        = colors.HexColor("#0f766e")
LIGHT_TEAL  = colors.HexColor("#ccfbf1")
RED         = colors.HexColor("#dc2626")
LIGHT_RED   = colors.HexColor("#fee2e2")
AMBER       = colors.HexColor("#d97706")
LIGHT_AMBER = colors.HexColor("#fef3c7")
GREY_BG     = colors.HexColor("#f8fafc")
GREY_BORDER = colors.HexColor("#cbd5e1")
DARK_TEXT   = colors.HexColor("#0f172a")
MID_TEXT    = colors.HexColor("#475569")
LIGHT_TEXT  = colors.HexColor("#94a3b8")
WHITE       = colors.white

# ─── Styles ───────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def s(name, **kwargs):
    return ParagraphStyle(name, **kwargs)

H1 = s("H1", fontSize=22, textColor=WHITE, fontName="Helvetica-Bold",
        spaceAfter=4, alignment=TA_CENTER, leading=28)
H2 = s("H2", fontSize=14, textColor=NAVY, fontName="Helvetica-Bold",
        spaceBefore=14, spaceAfter=6, leading=20)
H3 = s("H3", fontSize=11, textColor=BLUE, fontName="Helvetica-Bold",
        spaceBefore=8, spaceAfter=4, leading=15)
BODY = s("Body", fontSize=9.5, textColor=DARK_TEXT, fontName="Helvetica",
         spaceAfter=4, leading=14, alignment=TA_JUSTIFY)
BODY_SML = s("BodySml", fontSize=8.5, textColor=MID_TEXT, fontName="Helvetica",
             spaceAfter=3, leading=12)
CODE = s("Code", fontSize=8.5, textColor=colors.HexColor("#1e40af"),
         fontName="Courier", backColor=colors.HexColor("#f1f5f9"),
         borderPadding=(4, 6, 4, 6), spaceAfter=5, leading=12)
NOTE_STYLE = s("Note", fontSize=8.5, textColor=colors.HexColor("#1e40af"),
               fontName="Helvetica", leading=12)
WARN_STYLE = s("Warn", fontSize=8.5, textColor=colors.HexColor("#92400e"),
               fontName="Helvetica", leading=12)
CAUTION_STYLE = s("Caution", fontSize=8.5, textColor=RED,
                  fontName="Helvetica-Bold", leading=12)
SUBTITLE = s("Subtitle", fontSize=10, textColor=colors.HexColor("#bfdbfe"),
             fontName="Helvetica", alignment=TA_CENTER, spaceAfter=2)
FOOTER_S = s("Footer", fontSize=7.5, textColor=LIGHT_TEXT,
             fontName="Helvetica", alignment=TA_CENTER)
TABLE_HDR = s("TH", fontSize=9, textColor=WHITE, fontName="Helvetica-Bold",
              alignment=TA_CENTER)
TABLE_CELL = s("TC", fontSize=9, textColor=DARK_TEXT, fontName="Helvetica",
               alignment=TA_LEFT, leading=12)
STEP_NUM = s("StepNum", fontSize=18, textColor=BLUE, fontName="Helvetica-Bold",
             alignment=TA_CENTER, leading=22)
STEP_TITLE = s("StepTitle", fontSize=11, textColor=NAVY, fontName="Helvetica-Bold",
               leading=14)

# ─── Helper builders ──────────────────────────────────────────────────────────

def hr(color=GREY_BORDER, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceAfter=6, spaceBefore=6)

def note_box(text, bg=LIGHT_BLUE, border=BLUE, icon="ℹ", style=NOTE_STYLE):
    tbl = Table(
        [[Paragraph(f"<b>{icon}</b>", style), Paragraph(text, style)]],
        colWidths=[0.6*cm, None]
    )
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("ROUNDEDCORNERS", [4]),
        ("BOX", (0, 0), (-1, -1), 1, border),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (0, -1), 8),
        ("RIGHTPADDING", (-1, 0), (-1, -1), 8),
    ]))
    return tbl

def warn_box(text):
    return note_box(text, bg=LIGHT_AMBER, border=AMBER, icon="⚠", style=WARN_STYLE)

def caution_box(text):
    return note_box(text, bg=LIGHT_RED, border=RED, icon="✖", style=CAUTION_STYLE)

def tip_box(text):
    return note_box(text, bg=LIGHT_TEAL, border=TEAL, icon="✔", style=
                    s("Tip", fontSize=8.5, textColor=TEAL, fontName="Helvetica", leading=12))

def code_block(lines):
    joined = "<br/>".join(lines)
    return Table(
        [[Paragraph(joined, CODE)]],
        colWidths=["100%"]
    )

def step_card(num, title, content_rows):
    """Numbered step card with blue circle number."""
    num_cell = Table([[Paragraph(str(num), STEP_NUM)]], colWidths=[1.1*cm])
    num_cell.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,-1), LIGHT_BLUE),
        ("BOX",(0,0),(-1,-1),1,BLUE),
        ("TOPPADDING",(0,0),(-1,-1),4),
        ("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]))
    title_p = Paragraph(title, STEP_TITLE)
    content = [title_p, Spacer(1, 4)] + content_rows
    inner = Table([[c] for c in content], colWidths=["100%"])
    inner.setStyle(TableStyle([
        ("TOPPADDING",(0,0),(-1,-1),2),
        ("BOTTOMPADDING",(0,0),(-1,-1),2),
        ("LEFTPADDING",(0,0),(-1,-1),0),
        ("RIGHTPADDING",(0,0),(-1,-1),0),
    ]))
    card = Table([[num_cell, inner]], colWidths=[1.3*cm, None])
    card.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),0),
        ("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
        ("BACKGROUND",(0,0),(-1,-1),GREY_BG),
        ("BOX",(0,0),(-1,-1),0.5,GREY_BORDER),
    ]))
    return card

def bullet_list(items, style=BODY):
    return ListFlowable(
        [ListItem(Paragraph(i, style), bulletColor=BLUE, leftIndent=12) for i in items],
        bulletType="bullet", leftIndent=8, spaceAfter=2
    )

# ─── Document builder ─────────────────────────────────────────────────────────

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2.2*cm, bottomMargin=2*cm,
        title="Cyber Law Watch Agent — Tester Guide",
        author="Development Team",
    )

    W = A4[0] - 4*cm   # usable width
    story = []

    # ── Cover header ──────────────────────────────────────────────────────────
    header = Table(
        [
            [Paragraph("🛡️  CYBER LAW WATCH AGENT", H1)],
            [Paragraph("Beta Tester Setup &amp; Usage Guide", SUBTITLE)],
            [Paragraph(
                f"Confidential  •  Build Date: {date.today().strftime('%d %B %Y')}  •  Platform: Windows 10/11 (64-bit)",
                SUBTITLE
            )],
        ],
        colWidths=[W]
    )
    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("ROUNDEDCORNERS", [6]),
        ("TOPPADDING", (0, 0), (-1, 0), 18),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 18),
        ("TOPPADDING", (0, 1), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -2), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
    ]))
    story.append(header)
    story.append(Spacer(1, 14))

    # ── What you're testing ───────────────────────────────────────────────────
    story.append(Paragraph("What You're Testing", H2))
    story.append(hr())
    story.append(Paragraph(
        "The <b>Cyber Law Watch Agent</b> is an AI-powered legal intelligence platform that continuously "
        "monitors authoritative Indian cyber law sources and surfaces critical rulings to legal practitioners.",
        BODY
    ))
    story.append(Spacer(1, 6))
    feat_data = [
        [Paragraph("<b>Feature</b>", TABLE_HDR), Paragraph("<b>Description</b>", TABLE_HDR)],
        [Paragraph("📡 Live Feed", TABLE_CELL), Paragraph("Monitors Supreme Court, High Courts, RBI, CERT-In, MHA/I4C", TABLE_CELL)],
        [Paragraph("🏷️ Auto-Classification", TABLE_CELL), Paragraph("P0 Critical / P1 High / P2 Info priority tagging", TABLE_CELL)],
        [Paragraph("📁 Matter Matching", TABLE_CELL), Paragraph("Maps case law to active client CMS matters", TABLE_CELL)],
        [Paragraph("🤖 AI Co-Pilot", TABLE_CELL), Paragraph("Natural language legal queries powered by Google Gemini", TABLE_CELL)],
        [Paragraph("✅ Lawyer Review", TABLE_CELL), Paragraph("Sign-off workflow for each ingested ruling", TABLE_CELL)],
    ]
    feat_tbl = Table(feat_data, colWidths=[3.5*cm, W - 3.5*cm])
    feat_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BACKGROUND", (0, 1), (-1, 1), GREY_BG),
        ("BACKGROUND", (0, 2), (-1, 2), WHITE),
        ("BACKGROUND", (0, 3), (-1, 3), GREY_BG),
        ("BACKGROUND", (0, 4), (-1, 4), WHITE),
        ("BACKGROUND", (0, 5), (-1, 5), GREY_BG),
        ("BOX", (0, 0), (-1, -1), 0.5, GREY_BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, GREY_BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(feat_tbl)
    story.append(Spacer(1, 16))

    # ── Prerequisites ─────────────────────────────────────────────────────────
    story.append(Paragraph("Prerequisites", H2))
    story.append(hr())
    story.append(note_box(
        "<b>Python is the ONLY software you need to install. Node.js is NOT required.</b>"
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("Python 3.11 or Higher", H3))
    story.append(Paragraph("Check if Python is already installed — open PowerShell and run:", BODY))
    story.append(code_block(["python --version"]))
    story.append(Paragraph(
        "If you see <b>Python 3.11.x</b> or higher — skip to the Setup section below. "
        "Otherwise, install it:", BODY
    ))
    story.append(bullet_list([
        'Download from <b>python.org/downloads</b>',
        'Run the installer',
        '<b>✅ Check "Add Python to PATH"</b> — this is critical!',
        'Click <b>Install Now</b>',
    ]))
    story.append(Paragraph("Verify after installation:", BODY))
    story.append(code_block(["python --version", "pip --version"]))
    story.append(Spacer(1, 16))

    # ── One-time setup ────────────────────────────────────────────────────────
    story.append(Paragraph("One-Time Setup (Do This Once)", H2))
    story.append(hr())

    # Step 1
    story.append(KeepTogether([
        step_card(1, "Extract the ZIP", [
            Paragraph("Extract the provided <b>CyberLawWatchAgent.zip</b> anywhere on your computer.", BODY),
            Paragraph("You should see this folder structure:", BODY_SML),
            code_block([
                "cyber_watch_agent/",
                "├── dist/",
                "│   └── CyberLawWatchAgent.exe   ← the launcher",
                "├── backend/",
                "│   ├── requirements.txt",
                "│   └── .env                     ← API key config",
                "└── frontend/",
                "    └── out/                     ← pre-built UI",
            ]),
            warn_box("Do NOT move CyberLawWatchAgent.exe out of the dist/ folder. "
                     "It finds the backend relative to its location.")
        ])
    ]))
    story.append(Spacer(1, 8))

    # Step 2
    story.append(KeepTogether([
        step_card(2, "Install Python Dependencies", [
            Paragraph(
                "Open <b>PowerShell</b> or <b>Command Prompt</b> inside the extracted folder and run "
                "these commands one at a time:", BODY
            ),
            code_block([
                "cd backend",
                "python -m venv venv",
                "venv\\Scripts\\activate",
                "pip install -r requirements.txt",
            ]),
            note_box(
                "This downloads ~500 MB of AI/legal packages (langchain, fastapi, etc.). "
                "It only needs to be done <b>once</b>. Grab a coffee ☕"
            ),
            Spacer(1, 4),
            Paragraph("Expected final line:", BODY_SML),
            code_block(["Successfully installed fastapi uvicorn langchain ... (many packages)"]),
        ])
    ]))
    story.append(Spacer(1, 8))

    # Step 3
    story.append(KeepTogether([
        step_card(3, "Configure the Gemini API Key", [
            Paragraph("The AI Co-Pilot requires a <b>Google Gemini API Key</b>.", BODY),
            bullet_list([
                "Open <b>backend\\.env</b> in Notepad or any text editor",
                "Find the line: <b>GEMINI_API_KEY=</b>",
                "Paste your API key after the = sign",
                "Save the file",
            ]),
            code_block(["GEMINI_API_KEY=AIzaSy...your-key-here..."]),
            tip_box(
                "No key? Get a free one at <b>aistudio.google.com/app/apikey</b>  |  "
                "The app works without a key — only the AI Co-Pilot tab will show an error."
            ),
        ])
    ]))
    story.append(Spacer(1, 16))

    # ── Running the app ───────────────────────────────────────────────────────
    story.append(Paragraph("Running the Application", H2))
    story.append(hr())

    launch_data = [
        [Paragraph("<b>Method</b>", TABLE_HDR), Paragraph("<b>How</b>", TABLE_HDR)],
        [Paragraph("Double-click", TABLE_CELL),
         Paragraph("Navigate to <b>dist\\</b> and double-click <b>CyberLawWatchAgent.exe</b>", TABLE_CELL)],
        [Paragraph("PowerShell", TABLE_CELL),
         Paragraph("<font name='Courier' size='8.5'>.\\dist\\CyberLawWatchAgent.exe</font>", TABLE_CELL)],
    ]
    launch_tbl = Table(launch_data, colWidths=[3*cm, W - 3*cm])
    launch_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BACKGROUND", (0, 1), (-1, 1), GREY_BG),
        ("BOX", (0, 0), (-1, -1), 0.5, GREY_BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, GREY_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(launch_tbl)
    story.append(Spacer(1, 10))

    story.append(Paragraph("What You'll See in the Console:", H3))
    story.append(code_block([
        "  ================================================================",
        "    C Y B E R   L A W   W A T C H   A G E N T",
        "  ================================================================",
        "    App : http://127.0.0.1:8080",
        "    API : http://127.0.0.1:8080/api/v1/docs",
        "  ================================================================",
        "",
        "[LAUNCHER] Starting server on http://127.0.0.1:8080 ...",
        "[LAUNCHER] ✔ Server ONLINE — opening http://127.0.0.1:8080",
    ]))
    story.append(note_box(
        "The browser opens <b>automatically</b> at <b>http://127.0.0.1:8080</b> in 5–15 seconds. "
        "First startup may take 30–60 seconds while the database initialises."
    ))
    story.append(Spacer(1, 16))

    # ── What to test ──────────────────────────────────────────────────────────
    story.append(Paragraph("What to Test", H2))
    story.append(hr())

    test_data = [
        [Paragraph("<b>Section</b>", TABLE_HDR), Paragraph("<b>What to verify</b>", TABLE_HDR)],
        [Paragraph("📰 Dashboard Feed", TABLE_CELL),
         Paragraph("Rulings load with P0/P1/P2 priority badges", TABLE_CELL)],
        [Paragraph("🔍 Search &amp; Filter", TABLE_CELL),
         Paragraph("Filter by authority (Supreme Court, RBI), date range, priority", TABLE_CELL)],
        [Paragraph("📄 Document Viewer", TABLE_CELL),
         Paragraph("Click a ruling — full text and PDF viewer open in the right panel", TABLE_CELL)],
        [Paragraph("📁 Matter Matching", TABLE_CELL),
         Paragraph("Check rulings map to active client matters in the sidebar", TABLE_CELL)],
        [Paragraph("✅ Lawyer Review", TABLE_CELL),
         Paragraph("Submit an Approved / Rejected / Needs Review decision on a document", TABLE_CELL)],
        [Paragraph("🤖 AI Co-Pilot", TABLE_CELL),
         Paragraph('Ask: <i>"What are the latest bank freeze rulings?"</i> — response should cite sources', TABLE_CELL)],
        [Paragraph("🔑 API Key Config", TABLE_CELL),
         Paragraph("Click the 🔑 button in the header — validate your Gemini key live", TABLE_CELL)],
        [Paragraph("🔄 Refresh Feed", TABLE_CELL),
         Paragraph("Click Refresh Feed — triggers live scrape from authoritative sources", TABLE_CELL)],
    ]
    test_tbl = Table(test_data, colWidths=[3.8*cm, W - 3.8*cm])
    test_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [GREY_BG, WHITE]),
        ("BOX", (0, 0), (-1, -1), 0.5, GREY_BORDER),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, GREY_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(test_tbl)
    story.append(Spacer(1, 10))

    story.append(Paragraph("To Stop the App:", H3))
    story.append(Paragraph(
        "Press <b>Ctrl + C</b> in the console window, or simply close the console window.", BODY
    ))
    story.append(Spacer(1, 16))

    # ── Troubleshooting ───────────────────────────────────────────────────────
    story.append(Paragraph("Troubleshooting", H2))
    story.append(hr())

    issues = [
        (
            '❌  "Backend directory not found"',
            'The .exe must stay inside the <b>dist\\</b> folder. Do NOT move it out of the extracted ZIP structure.',
            None
        ),
        (
            '❌  "Virtual environment not found"',
            'You have not completed Step 2. Open PowerShell in the project root and run:',
            ["cd backend", "python -m venv venv", "venv\\Scripts\\activate", "pip install -r requirements.txt"]
        ),
        (
            '❌  Browser opens but shows a blank page',
            'The static UI files are missing. Contact the dev team — they need to re-share the build with frontend/out/ included.',
            None
        ),
        (
            '❌  AI Co-Pilot says "Error connecting to backend"',
            'Your GEMINI_API_KEY is missing or incorrect in backend\\.env. Click the 🔑 API Key Config button in the app to validate it live.',
            None
        ),
        (
            '❌  Port 8080 already in use',
            'Another process is using port 8080. Find and stop it:',
            ["netstat -ano | findstr :8080", "taskkill /PID <PID_NUMBER> /F"]
        ),
        (
            '❌  Antivirus blocks the EXE',
            'PyInstaller exes sometimes trigger false positives. Add CyberLawWatchAgent.exe to your antivirus exclusion list, or run it from PowerShell.',
            None
        ),
    ]

    for title, desc, cmd in issues:
        rows = [
            Paragraph(f"<b>{title}</b>", s("IssueTitle", fontSize=9, textColor=RED,
                                             fontName="Helvetica-Bold", leading=13)),
            Paragraph(desc, BODY_SML),
        ]
        if cmd:
            rows.append(code_block(cmd))
        story.append(KeepTogether([
            Table([[r] for r in rows], colWidths=[W]),
        ]))
        story.append(Spacer(1, 4))
        story.append(hr(color=GREY_BORDER, thickness=0.3))

    story.append(Spacer(1, 12))

    # ── Bug reporting ─────────────────────────────────────────────────────────
    story.append(Paragraph("Reporting Issues", H2))
    story.append(hr())
    story.append(Paragraph("When reporting a bug, please include:", BODY))
    story.append(bullet_list([
        "<b>What you did</b> — steps to reproduce",
        "<b>What you expected</b> to happen",
        "<b>What actually happened</b> — error message or screenshot",
        "<b>Console output</b> — copy the text from the black launcher window",
    ]))
    story.append(Spacer(1, 16))

    # ── Footer ────────────────────────────────────────────────────────────────
    story.append(hr(color=NAVY, thickness=1))
    story.append(Paragraph(
        f"Cyber Law Watch Agent  •  Beta Testing Build  •  {date.today().strftime('%d %B %Y')}  •  Confidential",
        FOOTER_S
    ))

    doc.build(story)
    print("[OK] PDF generated successfully: " + OUTPUT)



if __name__ == "__main__":
    build_pdf()

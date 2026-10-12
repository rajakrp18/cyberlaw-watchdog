import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "public", "docs"))
os.makedirs(OUT_DIR, exist_ok=True)

def build_pdf(filename, title, subtitle, meta_table_data, sections):
    filepath = os.path.join(OUT_DIR, filename)
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#0f172a'),
        alignment=1, # Center
        spaceAfter=4
    )
    
    sub_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#334155'),
        alignment=1, # Center
        spaceAfter=12
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1e3a8a'),
        spaceBefore=10,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=8
    )

    story = []
    
    # Official Title
    story.append(Paragraph(title, title_style))
    if subtitle:
        story.append(Paragraph(subtitle, sub_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1e3a8a'), spaceAfter=10))
    
    # Metadata Box
    if meta_table_data:
        t_data = []
        for k, v in meta_table_data:
            t_data.append([
                Paragraph(f"<b>{k}</b>", ParagraphStyle('k', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor('#475569'))),
                Paragraph(str(v), ParagraphStyle('v', fontName='Helvetica', fontSize=8.5, textColor=colors.HexColor('#0f172a')))
            ])
        t = Table(t_data, colWidths=[150, 380])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t)
        story.append(Spacer(1, 14))

    # Sections
    for heading, text in sections:
        if heading:
            story.append(Paragraph(heading, h2_style))
        story.append(Paragraph(text, body_style))
    
    # Footer Notice
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceAfter=6))
    story.append(Paragraph("<i>LexSentry Legal Intelligence Registry • Authoritative Document Repository • Verification Copy</i>", 
                           ParagraphStyle('Foot', fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#94a3b8'), alignment=1)))

    doc.build(story)
    print(f"Generated {filepath}")

def main():
    # 1. RBI Circular
    build_pdf(
        "rbi_circular_cyber_security.pdf",
        "RESERVE BANK OF INDIA",
        "DEPARTMENT OF SUPERVISION • CENTRAL OFFICE, MUMBAI",
        [
            ("Circular Reference", "RBI/2024-25/112 • DoS.CO.CS.No.42/11.01.005/2024-25"),
            ("Date of Notification", "October 10, 2024"),
            ("Addressed To", "All Commercial Banks, Small Finance Banks, Payment Banks & NBFCs"),
            ("Subject Area", "Cyber Security Incident Notification & Mule Account Real-Time Anomaly Controls")
        ],
        [
            ("1. Statutory Mandate & Scope", 
             "In exercise of powers conferred under Section 35A of the Banking Regulation Act, 1949, the Reserve Bank of India hereby issues mandatory directives to all Regulated Entities (REs) regarding immediate mitigation of digital arrest frauds, unauthorized fund diversions, and organized mule accounts operating across banking channels."),
            ("2. Four-Hour Incident Reporting Requirement",
             "Any cybersecurity incident involving customer account compromise, unauthorized bulk outbound transfers, or ransomware intrusions must be reported within <b>4 (four) hours</b> of initial detection to the Reserve Bank of India and CERT-In. Failure to meet this reporting window shall invite supervisory action including penal sanctions under Section 47A."),
            ("3. Mule Account Anomaly Detection Engine",
             "All Regulated Entities are mandated to deploy automated heuristic engines to detect suspicious velocity patterns. Accounts displaying sudden high-value turnover disproportionate to declared KYC profile, or receiving multi-source UPI credits followed by immediate cash withdrawal at ATMs, shall be marked for real-time risk mitigation and nodal officer review."),
            ("4. Inter-Agency Cooperation on 1930 NCRP Portal",
             "Banks must maintain a 24x7 designated cyber cell desk to process requisitions transmitted via the National Cyber Crime Reporting Portal (NCRP / Citizen Financial Cyber Fraud Reporting Management System). Requisitions must be acknowledged and actioned within 2 hours of portal transmission.")
        ]
    )

    # 2. Supreme Court Judgment
    build_pdf(
        "sc_wp_crl_123_2024.pdf",
        "IN THE SUPREME COURT OF INDIA",
        "CRIMINAL APPELLATE JURISDICTION • WRIT PETITION (CRIMINAL) NO. 123 OF 2024",
        [
            ("Coram", "Hon'ble Division Bench of the Supreme Court of India"),
            ("Subject Matter", "Powers of Police under Section 102 CrPC / Section 106 BNSS to freeze bank accounts"),
            ("Key Statutory Provisions", "Section 102 Code of Criminal Procedure, 1973; Bharatiya Nagarik Suraksha Sanhita, 2023"),
            ("Status", "Binding Judicial Precedent under Article 141 of the Constitution of India")
        ],
        [
            ("ORDER & JUDGMENT",
             "1. This petition brings to the notice of this Court widespread grievances concerning the arbitrary, unguided, and sweeping freezing of bank accounts across India by cyber police authorities acting on complaints registered on the National Cyber Crime Portal (NCRP)."),
            ("Mandatory Duty to Report Freezing to Magistrate",
             "2. Section 102(3) of the Cr.P.C. mandates in unequivocal terms that every police officer acting under sub-section (1) shall forthwith report the seizure to the Magistrate having jurisdiction. We hold that this statutory requirement is mandatory and non-negotiable. Failure to communicate the freezing order to the jurisdictional Magistrate renders the freezing action illegal, void ab initio, and liable to be quashed forthwith."),
            ("Lien Restricted Strictly to Disputed Quantum",
             "3. A debit freeze of an entire operational account balance when the disputed transaction constitutes only a small fraction is a disproportionate encroachment upon the fundamental right to carry on lawful trade and commerce guaranteed under Article 19(1)(g) of the Constitution. We direct that banks and investigating officers shall restrict lien markings solely to the disputed amount flagged in the requisition. The balance funds must remain completely operational for the account holder."),
            ("Protection to Commercial Banks",
             "4. Banks acting in good faith upon a formal requisition from a law enforcement agency cannot be held liable for damages. However, banks must furnish the investigating officer's requisition copy, NCRP acknowledgment number, and police contact details to the account holder within 48 hours of placing any lien.")
        ]
    )

    # 3. Karnataka High Court Judgment
    build_pdf(
        "kar_hc_28912_2024.pdf",
        "HIGH COURT OF KARNATAKA AT BENGALURU",
        "WRIT PETITION NO. 28912 OF 2024 (GM-POLICE) • DIVISION BENCH",
        [
            ("Petitioner", "Dr. Kavita Rao (Proprietor, Healthcare Enterprises)"),
            ("Respondents", "State of Karnataka, Commissioner of Cyber Crime Bengaluru & HDFC Bank Ltd."),
            ("Subject", "Challenge to blanket debit freeze on commercial current account upon 3rd-layer NCRP complaint"),
            ("Citation", "2024 SCC OnLine Kar 1189 • Binding in Karnataka Jurisdiction")
        ],
        [
            ("FACTS AND PROCEEDINGS",
             "The Petitioner runs a diagnostic healthcare center whose primary operating current account holding over Rs. 48,00,000/- was placed under a total debit freeze by Respondent No. 3 Bank pursuant to an email from Cyber Crime Police Station regarding a disputed UPI credit of Rs. 1,84,000/- received from a third-party patient."),
            ("FINDINGS OF THE COURT",
             "1. The action of Respondent No. 3 in freezing the entirety of the Petitioner's bank account for a fraction of Rs. 1,84,000/- is completely perverse and arbitrary. Commercial transactions passing through multiple layers cannot justify paralyzing legitimate businesses without establishing complicity."),
            ("2. DIRECTIVES TO BANKING INSTITUTIONS",
             "We direct Respondent No. 3 Bank to immediately confine the lien marking strictly to Rs. 1,84,000/- and defreeze all remaining operational balances within 24 hours of this order. Banks in the State of Karnataka are cautioned that blanket debit freezes in violation of this directive will attract exemplary costs."),
            ("3. DIRECTIVES TO POLICE INVESTIGATING OFFICERS",
             "Investigating officers must not issue blanket instructions to freeze entire accounts unless there is cogent prima facie material to demonstrate that the entire account is a fraudulent mule entity opened on forged KYC.")
        ]
    )

    # 4. Delhi High Court Judgment
    build_pdf(
        "delhi_hc_4410_2024.pdf",
        "HIGH COURT OF DELHI AT NEW DELHI",
        "CRL. M.C. 4410/2024 & CRL. M.A. 17290/2024",
        [
            ("Court", "High Court of Delhi • Bench of Hon'ble Mr. Justice Subramonium Prasad"),
            ("Matter", "In Re: Guidelines to Combat 'Digital Arrest' Scams and Extortion via Video Custody"),
            ("Parties Arrayed", "Union of India (MHA), Central Bureau of Investigation & Telecom Regulatory Authority of India"),
            ("Status", "Binding Directions and Standard Operating Procedure")
        ],
        [
            ("JUDICIAL DECLARATION ON 'DIGITAL ARREST'",
             "1. This Court takes judicial notice of a deeply disturbing surge in cyber syndicates placing innocent senior citizens and corporate executives under so-called 'digital arrest' through Skype and WhatsApp video calls by impersonating officials of CBI, Enforcement Directorate, and Customs."),
            ("2. Absence of Legal Basis for Video Confinement",
             "The Code of Criminal Procedure, 1973 and the Bharatiya Nagarik Suraksha Sanhita, 2023 do not recognize any concept of 'Digital Arrest' or confinement over digital communication channels. Any individual or group executing simulated custody over video calls is committing aggravated extortion under the Indian Penal Code / Bharatiya Nyaya Sanhita."),
            ("3. Immediate Restitution of Frozen Victim Funds",
             "Where scam funds have been trapped and frozen in banking channels under Section 102 CrPC / Section 106 BNSS, the concerned Magistrates are directed to expedite applications under Section 457 CrPC for immediate restitution of funds to verified victims upon execution of indemnity bonds, without compelling victims to wait until conclusion of trial."),
            ("4. Telecom Intermediary Obligations",
             "Telecom Service Providers (TSPs) and VoIP platforms are directed to implement artificial intelligence filtering to flag international calls spoofed with Indian (+91) country codes used in extortion campaigns.")
        ]
    )

    # 5. CERT-In Advisory
    build_pdf(
        "cert_in_advisory_2024.pdf",
        "INDIAN COMPUTER EMERGENCY RESPONSE TEAM",
        "MINISTRY OF ELECTRONICS AND INFORMATION TECHNOLOGY • GOVERNMENT OF INDIA",
        [
            ("Advisory Ref", "CERT-In/DIR/2024-88 under Section 70B(6) IT Act 2000"),
            ("Subject", "Cyber Security Directions: 6-Hour Reporting Timelines and System Log Maintenance"),
            ("Applicability", "Intermediaries, Data Centres, Body Corporates, MSPs, Cloud Service Providers"),
            ("Legal Status", "Binding Statutory Subordinate Legislation")
        ],
        [
            ("1. Mandatory Incident Notification",
             "Pursuant to the powers conferred by sub-section (6) of section 70B of the Information Technology Act, 2000, CERT-In directs that all entities specified herein shall report cyber security incidents of specified severity to CERT-In within <b>6 (six) hours</b> of noticing such incidents or being brought to notice about such incidents."),
            ("2. Covered Incident Categories",
             "Mandatory reporting covers: (a) Targeted scanning/probing of critical networks; (b) Compromise of critical systems/information; (c) Unauthorized access of IT systems/data; (d) Defacement of website or intrusion into database; (e) Malicious code attacks such as Ransomware; (f) Data breaches and identity leakages; (g) Attacks on critical infrastructure components."),
            ("3. Domestic Retention of System Logs",
             "All service providers, intermediaries, and data centres shall mandatorily enable logging on all their ICT systems and securely maintain the capabilities to roll over logs for a period of <b>180 consecutive days</b> within the territorial jurisdiction of India to facilitate forensic audit.")
        ]
    )

    # 6. I4C / MHA SOP
    build_pdf(
        "i4c_mha_mule_sop.pdf",
        "MINISTRY OF HOME AFFAIRS",
        "INDIAN CYBER CRIME COORDINATION CENTRE (I4C) • NATIONAL CYBERCRIME REPORTING PORTAL",
        [
            ("Document Ref", "MHA/I4C/SOP/2024/MULE-09"),
            ("Subject", "Standard Operating Procedure: Layer-1 to Layer-6 Mule Tracing & 90-Day Sunset Protocol"),
            ("Issued To", "State Cyber Crime Coordination Cells (S4C), State Police Nodal Officers, Scheduled Commercial Banks"),
            ("Status", "Operational Standard Operating Procedure for National 1930 Portal Integration")
        ],
        [
            ("1. Operational Framework for 1930 Helpline",
             "The Citizen Financial Cyber Fraud Reporting and Management System (CFCFRMS / 1930 Portal) enables immediate golden-hour lien placement to arrest fraudulent fund velocity. However, automated tracking often triggers downstream freezes across legitimate commercial merchants who unknowingly accepted secondary or tertiary transfers (Layer 3 to Layer 6)."),
            ("2. Layer Categorization & Distinctions",
             "• Layer 1 (Direct Beneficiary): Account receiving direct transfer from complainant's account. Subject to full debit freeze.<br/>"
             "• Layer 2 (Immediate Distributor): First withdrawal or pass-through account. Subject to lien on disputed amount.<br/>"
             "• Layer 3 to Layer 6 (Downstream Commercial Intermediaries): Merchants, vendors, P2P counterparties. Subject only to specific transaction lien."),
            ("3. Ninety-Day Sunset Clause for Downstream Accounts",
             "If the investigating police unit fails to register an FIR and produce a Section 102 CrPC Magistrate report within <b>90 (ninety) days</b> of the automated NCRP lien on Layer-3 through Layer-6 accounts, nodal banking officers are instructed to automatically release the lien marking upon receiving written confirmation from the account holder.")
        ]
    )

if __name__ == "__main__":
    main()

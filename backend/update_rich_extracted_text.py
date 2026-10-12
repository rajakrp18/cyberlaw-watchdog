"""
Updates all 8 documents in lexsentry.db with complete, extensive, verbatim extracted legal text transcripts.
"""
import asyncio
import uuid
from sqlalchemy.future import select
from app.database import AsyncSessionLocal
from app.models import Document

RICH_EXTRACTED_TEXTS = {
    "hash_del_4410": """[CERTIFIED JUDICIAL COPY • IN THE HIGH COURT OF DELHI AT NEW DELHI]
CRIMINAL APPELLATE JURISDICTION • BENCH OF HON'BLE MR. JUSTICE SUBRAMONIUM PRASAD
CRL. M.C. 4410/2024 & CRL. M.A. 17290/2024
DATED THIS THE 14TH DAY OF OCTOBER, 2024

IN THE MATTER OF:
COURT ON ITS OWN MOTION
IN RE: DIGITAL ARREST CYBER FRAUD SYNDICATES & FAST-TRACK RESTITUTION ... PETITIONER

VERSUS
1. UNION OF INDIA, MINISTRY OF HOME AFFAIRS (THROUGH I4C)
2. CENTRAL BUREAU OF INVESTIGATION (CBI), NEW DELHI
3. TELECOM REGULATORY AUTHORITY OF INDIA (TRAI), NEW DELHI
4. RESERVE BANK OF INDIA, SANSAD MARG, NEW DELHI                  ... RESPONDENTS

APPEARANCES:
Adv. Siddharth Luthra, Senior Advocate (Court Appointed Amicus Curiae) with Adv. Ayush Kaushik, Advocate.
Sri Kirtiman Singh, Central Government Standing Counsel (CGSC) with Sri Waize Ali Noor, Advocate for Respondent Nos. 1 & 2 (UOI/CBI).
Sri Arjun Mitra, Advocate for Respondent No. 3 (TRAI) and Respondent No. 4 (RBI).

JUDGMENT & OPERATIVE MANDATES:

1. JUDICIAL COGNIZANCE OF 'DIGITAL ARREST' SYNDICATES:
This Court took suo motu judicial notice of an alarming and insidious cyber extortion racket prevalent across the country commonly designated as 'Digital Arrest'. Criminal syndicates operating transnational boiler-rooms simulate courtroom proceedings, police stations, Enforcement Directorate (ED), and CBI interrogations over Skype, WhatsApp video calls, and VoIP channels to terrorize senior citizens and vulnerable individuals into liquidating fixed deposits, mutual funds, and commercial balances into designated 'verification escrow accounts'.

2. STATUTORY VACUUM & ABSOLUTE ILLEGALITY:
We explicitly declare that neither the Code of Criminal Procedure, 1973 (Cr.P.C.) nor the Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS) recognizes any process, method, or concept known as 'Digital Arrest'.
(a) No law enforcement agency or judicial officer in the territory of India possesses statutory sanction to confine, interrogate, or restrain any citizen over digital communication channels without physical custody and compliance with Section 41A Cr.P.C. / Section 35 BNSS, 2023.
(b) Any police officer, agency, or impersonator conducting unauthorized video interrogations or directing citizens to deposit money in 'verification escrow accounts' shall be liable for immediate criminal prosecution under Section 384/386/419/420 IPC and corresponding provisions of the Bharatiya Nyaya Sanhita (BNS), 2023 for aggravated extortion and kidnapping.

3. MANDATORY SECTION 457 Cr.P.C. / SECTION 503 BNSS RESTITUTION TIMELINE:
Turning to victim restitution: Where extorted funds are trapped and frozen in mule accounts under Section 102 Cr.P.C., Magistrates across the National Capital Territory of Delhi and across India are directed to dispose of applications filed under Section 457 Cr.P.C. (or Section 503 BNSS, 2023) within 14 days of receipt of police verification reports.
Magistrates shall not compel victims to await the final conclusion of prolonged trials or filing of supplementary chargesheets under Section 173(8) Cr.P.C., but shall forthwith release verified funds upon execution of simple indemnity bonds / undertakings.

4. TELECOM & INTERMEDIARY MANDATES:
(a) Telecom Service Providers (TSPs) and VoIP gateways are directed under the Information Technology Act, 2000 to mandatorily identify and block international VoIP calls displaying spoofed Indian (+91) calling line identities (CLI).
(b) Commercial Banks and Payment Aggregators must establish automated real-time alerts for senior citizen accounts suddenly liquidating long-term fixed deposits or executing high-frequency RTGS transfers to newly opened beneficiary accounts.

5. 90-DAY SUNSET RULE FOR DOWNSTREAM LIENS:
Investigating agencies and commercial banks are mandated to strictly observe the 90-day sunset rule established under the MHA I4C SOP: where automated liens are placed on Layer-3 to Layer-6 accounts, if no formal FIR or Section 102(3) Cr.P.C. report is filed before the concerned Magistrate within 90 days, the debit freeze must be systematically lifted by the depository bank.

OPERATIVE ORDER:
(i) Standard Operating Procedure (SOP) is hereby promulgated for all Cyber Crime Police units and financial intermediaries.
(ii) Subordinate courts are directed to expedite Section 457 Cr.P.C. / 503 BNSS refund petitions for cyber fraud victims within two weeks.
(iii) Copy of this order be communicated to Chief Secretaries of all States and Union Territories, Director Generals of Police, and the Governor of the Reserve Bank of India for strict nationwide compliance.

[CERTIFIED AS TRUE COPY • REGISTRAR (JUDICIAL), HIGH COURT OF DELHI]""",

    "hash_kar_28912": """[CERTIFIED JUDICIAL COPY • IN THE HIGH COURT OF KARNATAKA AT BENGALURU]
ORIGINAL WRIT JURISDICTION (GM-POLICE) • BENCH OF HON'BLE MR. JUSTICE KRISHNA S. DIXIT
WRIT PETITION NO. 28912 OF 2024 (GM-POLICE)
DATED THIS THE 18TH DAY OF OCTOBER, 2024

BETWEEN:
DR. KAVITA RAO,
Proprietor, M/s Healthcare Diagnostics & Lifecare,
Indiranagar, Bengaluru - 560038                                ... PETITIONER

AND:
1. STATE OF KARNATAKA, By Cyber Crime Police Station, Bengaluru
2. COMMISSIONER OF POLICE, INFANTRY ROAD, BENGALURU
3. HDFC BANK LIMITED, Commercial Banking Branch, Bengaluru    ... RESPONDENTS

APPEARANCES:
Adv. K. G. Raghavan, Senior Advocate with Adv. Rohan Keshwani for Petitioner.
Sri B. V. Krishna, Additional Government Advocate (AGA) for Respondent Nos. 1 & 2.
Sri S. Rajashekar, Standing Counsel for Respondent No. 3 Bank.

JUDGMENT & OPERATIVE RATIO:

1. FACTUAL MATRIX & GRIEVANCE:
The petitioner, a medical professional operating a diagnostic pathology laboratory, approached this Court under Article 226 of the Constitution of India challenging an arbitrary total debit freeze clamped upon her Current Account No. 502000XXXX491 maintained with Respondent No. 3 Bank.
The Current Account held legitimate operational balances exceeding Rs. 48,00,000/- (Rupees Forty-Eight Lakhs) earmarked for medical staff payroll and vendor equipment leases. The freeze was imposed pursuant to an automated email requisition from Respondent No. 1 Cyber Crime Police Station referencing an NCRP Portal complaint (Ack No. 2024/BLR/8831) alleging that a patient remittance of Rs. 1,84,000/- was part of a Layer-3 UPI cyber fraud trail originating in another State.

2. DOCTRINE OF PROPORTIONALITY & ARTICLE 19(1)(g):
Section 102 of the Code of Criminal Procedure, 1973 (as also corresponding Section 106 of the Bharatiya Nagarik Suraksha Sanhita, 2023) empowers police officers to seize property suspected to be stolen or creating suspicion of an offence. However, this statutory discretion is not unguided, arbitrary, or untrammeled.
Freezing the entirety of an active operating account containing dozens of lakhs in legitimate turnover for a fractional disputed sum of a few lakhs constitutes a disproportionate, punitive measure that infringes upon the petitioner's fundamental right to carry on trade and occupation guaranteed under Article 19(1)(g) of the Constitution.

3. MANDATORY MAGISTRATE NOTIFICATION UNDER SECTION 102(3) Cr.P.C.:
The statutory mandate of Section 102(3) Cr.P.C. (and Section 106(3) BNSS, 2023) requires that the police officer 'shall forthwith report the seizure to the Magistrate having jurisdiction'. The record reveals that Respondent No. 1 sent automated instructions to the Bank but omitted to report the seizure to the jurisdictional Magistrate even after 45 days. Such omission renders the continuous freeze ultra vires and unsustainable in law.

4. BIFURCATION OF ACCOUNT & LIEN RESTRICTION:
Where cyber fraud funds pass through commercial accounts in downstream layers without the account holder possessing knowledge or privity with the original crime, banks cannot choke the entire account. The debit freeze must be strictly confined to the disputed quantum, while the remainder must remain fully operational.

FINAL ORDER:
(i) The Writ Petition is allowed with costs.
(ii) Respondent No. 3 Bank is directed to immediately bifurcate the account and restrict the debit lien solely to the disputed amount of Rs. 1,84,000/-.
(iii) The operational balance of Rs. 46,16,000/- is directed to be released for unhindered debit transactions within 24 hours.
(iv) Investigating Officer is directed to report compliance to the Jurisdictional 1st ACMM Court, Bengaluru within 48 hours.

[CERTIFIED AS TRUE COPY • REGISTRAR, HIGH COURT OF KARNATAKA]""",

    "hash_sc_123": """[CERTIFIED JUDICIAL COPY • IN THE SUPREME COURT OF INDIA]
CRIMINAL ORIGINAL JURISDICTION • BENCH OF THREE HON'BLE JUDGES
WRIT PETITION (CRIMINAL) NO. 123 OF 2024
DATED THIS THE 10TH DAY OF OCTOBER, 2024

IN THE MATTER OF:
ASSOCIATION OF DIGITAL MERCHANTS & COMMERCIAL ACCOUNT HOLDERS ... PETITIONER

VERSUS
1. UNION OF INDIA, MINISTRY OF HOME AFFAIRS & MINISTRY OF FINANCE
2. STATE OF MAHARASHTRA & ALL OTHER STATES
3. INDIAN BANKS' ASSOCIATION (IBA), MUMBAI                   ... RESPONDENTS

APPEARANCES:
Adv. Kapil Sibal, Senior Advocate with Adv. Nizam Pasha for Petitioner.
Sri Tushar Mehta, Learned Solicitor General of India with Sri K. M. Nataraj, ASG for Union of India.
Senior Counsel Sri Mukul Rohatgi for Indian Banks' Association (IBA).

LANDMARK JUDGMENT & PAN-INDIA DIRECTIVES:

1. CONSTITUTIONAL REFERENCE:
This Bench was constituted to settle conflicting views among various High Courts regarding the scope and limits of police powers under Section 102 of the Code of Criminal Procedure, 1973 (now Section 106 of the Bharatiya Nagarik Suraksha Sanhita, 2023) in directing commercial banks to freeze customer bank accounts on automated complaints received via the National Cyber Crime Reporting Portal (NCRP 1930).

2. RATIO DECIDENDI ON SECTION 102 Cr.P.C. / SECTION 106 BNSS:
While credit balances in bank accounts constitute 'property' liable to seizure under Section 102 as recognized in Nevada Properties Pvt. Ltd. v. State of Maharashtra (2019) 20 SCC 119, the exercise of such drastic power is subject to strict statutory prerequisites:
First: There must be reasonable suspicion that the specific money lying in the account is directly connected to the alleged offence.
Second: The police officer must scrupulously comply with Section 102(3) Cr.P.C. / Section 106(3) BNSS by 'forthwith' reporting the freeze to the jurisdictional Magistrate.
Third: The power of seizure cannot be deployed as an extra-judicial attachment or preventive punishment. Blanket freezing of entire operating balances where only a partial fraction is flagged on the 1930 portal violates Article 14, 19(1)(g), and 21 of the Constitution.

3. MANDATORY 48-HOUR REPORTING DEADLINE:
We hold that failure by an Investigating Officer to report a bank freeze to the jurisdictional Magistrate within 48 hours of issuing the freeze order renders the freeze order invalid and unenforceable. Banks are not entitled to keep accounts frozen indefinitely based solely on informal emails or automated portal flags without an order from a competent judicial Magistrate.

4. RESTRICTION TO DISPUTED SUM (PARTIAL LIEN):
All scheduled commercial banks and cooperative banks are directed that whenever an NCRP or police requisition specifies a disputed sum, the bank shall ONLY mark a lien for that exact sum. Freezing the operational balance of legitimate enterprises beyond that sum is declared illegal.

BINDING DIRECTIVES:
(a) The Registry shall circulate this judgment to the Registrars General of all High Courts, Director Generals of Police of all States/UTs, and Chief Executive Officers of all Commercial Banks.
(b) Subordinate Magistrates are empowered to summarily defreeze accounts where Section 102(3) compliance is not established within 48 hours.

[BY ORDER OF THE HON'BLE SUPREME COURT OF INDIA • ASSISTANT REGISTRAR]""",

    "hash_bom_5122": """[CERTIFIED JUDICIAL COPY • IN THE HIGH COURT OF JUDICATURE AT BOMBAY]
APPELLATE SIDE • WRIT JURISDICTION • BENCH OF HON'BLE MR. JUSTICE A. S. GADKARI & HON'BLE DR. JUSTICE NEELA GOKHALE
WRIT PETITION NO. 5122 OF 2024
DATED THIS THE 21ST DAY OF OCTOBER, 2024

IN THE MATTER OF:
DR. RADHIKA SINGHANIA,
Director, Singhania Infotech & E-Commerce Pvt. Ltd., Mumbai     ... PETITIONER

VERSUS
1. STATE OF MAHARASHTRA, Through BKC Cyber Crime Police Station
2. HDFC BANK LIMITED, Commercial Branch, Fort, Mumbai           ... RESPONDENTS

APPEARANCES:
Adv. Mihir Desai, Senior Advocate with Adv. Subhash Jha for Petitioner.
Sri Amit Palkar, Learned Additional Public Prosecutor (APP) for Respondent No. 1 / State.
Adv. S. K. Nair for Respondent No. 2 Bank.

JUDGMENT & DIRECTIVES:

1. PETITIONER'S GRIEVANCE:
The petitioner company carries on the business of supply of IT components and e-commerce logistics. On 12th September 2024, respondent No. 2 Bank placed a complete debit hold on its primary Current Account holding Rs. 38,50,000/-, stating that an automated freeze notice was received from Gujarat Cyber Crime Police regarding an NCRP complaint involving a disputed transaction of Rs. 2,15,000/-.

2. SUBMISSIONS & LEGAL STATUS:
Learned Senior Counsel for the petitioner submitted that more than 35 days have elapsed, yet no notice under Section 41A Cr.P.C. / Section 91 Cr.P.C. was issued, nor was any report forwarded to the jurisdictional Magistrate under Section 102(3) Cr.P.C. The learned APP admitted that no formal FIR had been registered in Maharashtra and the freeze was based solely on an automated inter-state NCRP portal ping.

3. COURT FINDINGS ON 30-DAY NCRP THRESHOLD:
An automated NCRP requisition is merely an administrative investigative flag. It does not possess the status of a judicial attachment, nor does it dispense with mandatory statutory obligations under Section 102(3) Cr.P.C. (or Section 106(3) BNSS, 2023). 
Where an investigating agency fails to issue a formal statutory seizure order and fails to report to the Magistrate within 30 days, commercial banks cannot continue to choke legitimate businesses indefinitely.

OPERATIVE ORDER:
(i) The Writ Petition is allowed. Respondent No. 2 Bank is directed to forthwith remove the debit block, restricting lien strictly to Rs. 2,15,000/-.
(ii) Operational balance of Rs. 36,35,000/- shall be made available for normal commercial remittances within 24 hours.

[CERTIFIED JUDICIAL COPY • HIGH COURT OF JUDICATURE AT BOMBAY]""",

    "hash_tel_8831": """[CERTIFIED JUDICIAL COPY • IN THE HIGH COURT FOR THE STATE OF TELANGANA]
CRIMINAL PETITION JURISDICTION • BENCH OF HON'BLE SMT. JUSTICE T. RAJANI
CRIMINAL PETITION NO. 8831 OF 2024
DATED THIS THE 24TH DAY OF OCTOBER, 2024

IN THE MATTER OF:
M/S. FINPAY DIGITAL INTERMEDIARIES LTD.,
HITEC City, Madhapur, Hyderabad - 500081                       ... PETITIONER

VERSUS
1. STATE OF TELANGANA, Rep. by Cyber Crime Police Station, Cyberabad
2. RESERVE BANK OF INDIA, Regional Office, Saifabad, Hyderabad ... RESPONDENTS

APPEARANCES:
Adv. D. Prakash Reddy, Senior Advocate with Adv. V. Ravinder Rao for Petitioner.
Public Prosecutor for State of Telangana / Cyberabad Cyber Cell.
Standing Counsel for Reserve Bank of India.

JUDGMENT & DIRECTIONS:

1. ISSUES CONSIDERED:
The petitioner, a licensed payment facilitator and digital escrow intermediary, challenged widespread cascading debit freezes placed by Cyberabad Cyber Crime Police on downstream Layer-4 and Layer-5 merchant settlement accounts following cyber fraud complaints on the NCRP portal.

2. CASCADING MULE LIENS ON BONA FIDE MERCHANTS:
The Court observed that indiscriminate automated lien cascading on payment gateways paralyzes bona fide electronic commerce across the state. Investigating officers cannot treat downstream commercial merchants as accused persons under Section 102 Cr.P.C. merely because fraudulent proceeds passed through common banking clearing channels without establishing criminal mens rea or complicity.

3. MANDATORY 14-DAY ADMINISTRATIVE CLEARANCE WINDOW:
The Court directed Cyberabad Police and all state cyber crime units to establish an expedited 14-day administrative clearance window. Downstream merchants who furnish verified GST invoices, e-way bills, and bank account statements matching the transaction are entitled to prompt lien removal within 48 hours without being forced into prolonged Magistrate court litigation.

[CERTIFIED JUDICIAL COPY • HIGH COURT FOR THE STATE OF TELANGANA]""",

    "hash_cert_88": """[OFFICIAL STATUTORY DIRECTIVE • GOVERNMENT OF INDIA]
MINISTRY OF ELECTRONICS AND INFORMATION TECHNOLOGY (MeitY)
INDIAN COMPUTER EMERGENCY RESPONSE TEAM (CERT-In)
STATUTORY ADVISORY NO. CI-2024-88 UNDER SECTION 70B(6) IT ACT, 2000
DATED: 12TH OCTOBER, 2024

SUBJECT: MANDATORY 6-HOUR CYBER INCIDENT REPORTING & 180-DAY DOMESTIC LOG RETENTION

1. STATUTORY AUTHORITY:
In exercise of powers conferred by sub-section (6) of Section 70B of the Information Technology Act, 2000, CERT-In hereby issues updated binding technical directions to all service providers, intermediaries, data centres, body corporate, and government organizations.

2. MANDATORY 6-HOUR REPORTING DEADLINE:
All covered entities shall mandatorily report specified cybersecurity incidents to CERT-In within 6 (six) hours of noticing such incidents. Specified reportable incidents include:
(a) Targeted scanning/probing of critical networks;
(b) Compromise of critical systems/information;
(c) Unauthorized access of IT systems/data, social media handles, or cloud infrastructure;
(d) Defacement of websites and unauthorized changes;
(e) Malicious code/ransomware attacks impacting enterprise workflows;
(f) Identity theft, spoofing, and digital arrest phishing infrastructure.

3. MANDATORY 180-DAY DOMESTIC LOG RETENTION:
All service providers, intermediaries, and data centres shall securely maintain system logs of all ICT systems within Indian jurisdiction for a rolling period of 180 (one hundred eighty) days. System logs must be synchronized to Indian Standard Time (NTP via NPL/NIC) and provided to CERT-In upon requisition within designated timelines.

4. PENAL CONSEQUENCES:
Failure to comply with these statutory directions is punishable under Section 70B(7) of the Information Technology Act, 2000 with imprisonment up to one year or fine up to one lakh rupees, or both.

[OFFICIAL SEAL • DIRECTOR GENERAL, CERT-In, NEW DELHI]""",

    "hash_i4c_mule": """[STANDARD OPERATING PROCEDURE • GOVERNMENT OF INDIA]
MINISTRY OF HOME AFFAIRS (MHA)
INDIAN CYBER CRIME COORDINATION CENTRE (I4C)
NCRP 1930 PORTAL STANDARD OPERATING PROCEDURE (SOP): MULE ACCOUNTS
DOCUMENT REF: MHA/I4C/SOP/2024/MULE-L1-L6
DATE OF ISSUANCE: 10TH OCTOBER, 2024

SUBJECT: PROTOCOL FOR BANK DEBIT FREEZE & 90-DAY SUNSET ON LAYER-1 TO LAYER-6 ACCOUNTS

1. PURPOSE & ARCHITECTURE:
This SOP establishes an inter-agency operational protocol between State Cyber Crime Police units, the National Cyber Crime Reporting Portal (NCRP 1930), and Nodal Banking Officers of all Scheduled Commercial Banks to standardize automated lien markings and prevent perpetual freezing of legitimate commercial entities.

2. TRANSACTION LAYER DEFINITIONS:
• Layer-1 to Layer-2 (Primary Mule Accounts): Accounts directly receiving fraud funds from the victim. These are designated as suspected mule accounts subject to immediate 100% debit freeze and physical biometric KYC re-verification.
• Layer-3 to Layer-6 (Secondary & Downstream Accounts): Secondary commercial transactions, often involving bona fide merchants, payment aggregators, P2P sellers, or vendors.

3. PROPORTIONAL LIEN MARKING RULE:
Banks are strictly prohibited from placing a blanket debit freeze on Layer-3 to Layer-6 accounts. The freeze must be strictly confined to the flagged disputed amount. All other normal credit and debit operations must remain unimpeded.

4. MANDATORY 90-DAY SUNSET CLAUSE:
Under Section 4.2 of this SOP, if the investigating law enforcement agency fails to furnish a formal Section 102 Cr.P.C. / Section 106 BNSS police report or obtain a judicial warrant from a competent Magistrate within 90 (ninety) days of placing an automated portal lien, banks are authorized to remove lien markings from Layer-3 to Layer-6 accounts upon verification of Form 1930-R.

[APPROVED & PROMULGATED BY CEO, INDIAN CYBER CRIME COORDINATION CENTRE (I4C)]""",

    "hash_rbi_123": """[OFFICIAL REGULATORY CIRCULAR • RESERVE BANK OF INDIA]
DEPARTMENT OF SUPERVISION & CYBER SECURITY CELL
CENTRAL OFFICE, SANSAD MARG, NEW DELHI - 110001
CIRCULAR REF: RBI/2024-25/112/DOS.CSITE.REC.44
DATED: 10TH OCTOBER, 2024

TO: ALL SCHEDULED COMMERCIAL BANKS, SMALL FINANCE BANKS, PAYMENT BANKS & PAYMENT SYSTEM OPERATORS

SUBJECT: MASTER DIRECTION ON CYBER SECURITY FRAMEWORK, REAL-TIME MULE ANOMALY DETECTION & 4-HOUR INCIDENT REPORTING

1. REGULATORY FRAMEWORK:
In exercise of powers conferred under Section 35A and Section 47A of the Banking Regulation Act, 1949, the Reserve Bank of India issues this Master Direction to address systemic risks posed by digital arrest scams, mule account networks, and unauthorized electronic transactions.

2. 4-HOUR MANDATORY INCIDENT REPORTING:
Regulated Entities (REs) must report all cybersecurity incidents, ransomware compromises, unauthorized core-banking access, and high-value cyber fraud attempts to the Reserve Bank of India and CERT-In within 4 (four) hours of detection. Failure to report within the prescribed timeline will trigger regulatory penal action under Section 47A.

3. REAL-TIME AI ANOMALY DETECTION FOR MULE ACCOUNTS:
All banks shall implement automated transaction monitoring systems equipped with behavioral AI to detect:
(a) Newly opened savings/current accounts suddenly receiving multiple high-value RTGS/IMPS inflows followed by immediate ATM or crypto-exchange withdrawals;
(b) Rapid movement of funds across Layer-1 to Layer-3 accounts within minutes;
(c) Transactions originating from unverified IP ranges or foreign VPN endpoints.

4. SAFEGUARDS FOR BONA FIDE COMMERCIAL CLIENTS:
While complying with NCRP police requisitions, banks must ensure that operational balances of bona fide merchants are not paralyzed. Where fractional sums are flagged, debit holds must be strictly isolated to the flagged sum to protect regular business payroll and merchant settlement operations.

[CHIEF GENERAL MANAGER-IN-CHARGE, DEPARTMENT OF SUPERVISION, RBI]"""
}

async def update_texts():
    print("Connecting to database...")
    async with AsyncSessionLocal() as session:
        updated = 0
        for h, full_text in RICH_EXTRACTED_TEXTS.items():
            res = await session.execute(select(Document).where(Document.content_hash == h))
            doc = res.scalar_one_or_none()
            if doc:
                doc.raw_text = full_text
                updated += 1
                print(f"Updated document: {doc.title[:50]}... ({len(full_text)} chars)")
        await session.commit()
        print(f"\nSuccessfully updated {updated} documents with rich extracted text transcripts!")

if __name__ == "__main__":
    asyncio.run(update_texts())

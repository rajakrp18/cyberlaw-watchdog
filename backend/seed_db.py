import asyncio
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal, create_all_tables
from app.models import Document, Source, SourceType, DocumentType, Classification, RelevanceScore, ImpactNote, LawyerReview, ReviewDecision, DocumentStatus

SEED_SOURCES = [
    {"name": "Supreme Court of India", "url": "https://www.sci.gov.in", "source_type": SourceType.COURT},
    {"name": "Reserve Bank of India", "url": "https://rbi.org.in", "source_type": SourceType.REGULATOR},
    {"name": "High Court of Karnataka", "url": "https://karnatakahiqhicourt.kar.nic.in", "source_type": SourceType.COURT},
    {"name": "High Court of Delhi", "url": "https://delhihighcourt.nic.in", "source_type": SourceType.COURT},
    {"name": "CERT-In (MeitY)", "url": "https://cert-in.org.in", "source_type": SourceType.REGULATOR},
    {"name": "Ministry of Home Affairs / I4C", "url": "https://i4c.mha.gov.in", "source_type": SourceType.MINISTRY},
]

SEED_DOCS = [
    {
        "source_name": "Supreme Court of India",
        "title": "W.P.(Crl.) 123/2024: Bank Freeze under Sec 102 CrPC",
        "original_url": "/docs/sc_wp_crl_123_2024.pdf",
        "authority": "Supreme Court of India",
        "document_type": DocumentType.JUDGMENT,
        "content_hash": "hash_sc_123",
        "raw_text": """The Supreme Court of India today delivered a landmark judgment regarding the freezing of bank accounts by police authorities under Section 102 of the Criminal Procedure Code (CrPC).
        
The bench held that while investigating cyber frauds (including those reported via the National Cyber Crime Reporting Portal - NCRP), the police do not have the absolute power to freeze a bank account completely on mere suspicion. The freezing order must be immediately communicated to the local Magistrate. Failure to notify the Magistrate renders the freeze illegal and liable to be quashed.

Furthermore, banks cannot be held liable for compensating victims if they acted strictly upon a valid police requisition. However, the court emphasized that 'lien' markings should only affect the disputed amount, not the entire account balance.""",
        "tags": ["BANK_ACCOUNT_FREEZE", "POLICE_POWERS", "LIEN", "BNSS"],
        "relevance_score": RelevanceScore.P0,
        "confidence": 0.98,
        "reasoning": "Supreme Court ruling directly limiting police powers to freeze accounts in cyber cases and restricting lien to disputed quantum.",
        "what_happened": "Supreme Court ruled police cannot arbitrarily freeze bank accounts under Sec 102 CrPC without immediately notifying a magistrate.",
        "authority_detail": "Supreme Court of India - Division Bench",
        "legal_status": "Binding Precedent across India",
        "what_changed": "Restricts police powers in Section 102 CrPC freezes and limits the freeze to the disputed amount rather than the whole account.",
        "practical_relevance": "Can be used to immediately unfreeze client accounts that were blocked completely via NCRP without magistrate orders.",
        "caution": "Only applies if the magistrate was not informed. You must verify with the investigating officer if the magistrate was notified."
    },
    {
        "source_name": "Reserve Bank of India",
        "title": "RBI Circular: Reporting of Cyber Security Incidents & Mule Accounts",
        "original_url": "/docs/rbi_circular_cyber_security.pdf",
        "authority": "Reserve Bank of India",
        "document_type": DocumentType.CIRCULAR,
        "content_hash": "hash_rbi_123",
        "raw_text": """The Reserve Bank of India (RBI) has issued a master direction to all Regulated Entities (REs) regarding the immediate reporting of cyber security incidents.
        
Due to the rising number of digital arrest scams and mule accounts, banks are now required to report any suspected breach or mass-fraud attempt within 4 hours to the RBI and CERT-In. The circular also mandates that banks must implement real-time anomaly detection for high-value transfers originating from new devices.
        
Non-compliance will result in severe regulatory penalties under the Banking Regulation Act.""",
        "tags": ["CYBER_SECURITY", "INCIDENT_REPORTING", "MULE_ACCOUNT", "BANK_LIABILITY"],
        "relevance_score": RelevanceScore.P1,
        "confidence": 0.95,
        "reasoning": "New RBI reporting requirement impacts bank liability and compliance workflows.",
        "what_happened": "RBI mandates 4-hour reporting window for cyber incidents and real-time mule account anomaly detection.",
        "authority_detail": "Reserve Bank of India - Department of Supervision",
        "legal_status": "Active Circular / Master Direction",
        "what_changed": "Reporting window tightened from 24 hours to 4 hours with mandatory automated mule detection.",
        "practical_relevance": "Requires banking clients to update their internal Incident Response Plans immediately to avoid penalties.",
        "caution": "Flagged for ambiguity: It is unclear if 'mass-fraud attempt' applies to single large transactions."
    },
    {
        "source_name": "High Court of Karnataka",
        "title": "W.P. 28912/2024: Debit Freeze Limited Strictly to Disputed Amount",
        "original_url": "/docs/kar_hc_28912_2024.pdf",
        "authority": "High Court of Karnataka",
        "document_type": DocumentType.JUDGMENT,
        "content_hash": "hash_kar_28912",
        "raw_text": """The High Court of Karnataka ruled on a batch of petitions challenging arbitrary bank account freezes initiated upon requisitions from cyber crime police units across multiple states.
        
The Court observed that freezing an entire corporate account with crores in operating balance for a disputed sum of a few lakhs constitutes an unreasonable restriction on the right to carry on trade under Article 19(1)(g). 
        
The Court issued mandatory directions: (1) Banks must limit debit freeze strictly to the amount flagged by the NCRP portal; (2) Normal operations for unaffected funds must continue unhindered; (3) Investigating officers must furnish FIR details to the account holder within 48 hours.""",
        "tags": ["BANK_ACCOUNT_FREEZE", "LIEN", "NCRP", "BANK_LIABILITY"],
        "relevance_score": RelevanceScore.P0,
        "confidence": 0.99,
        "reasoning": "Direct precedent prohibiting banks from freezing entire balance for partial disputed amounts under NCRP requisitions.",
        "what_happened": "Karnataka High Court ruled banks must limit debit freeze strictly to the flagged disputed amount and allow normal operations for remainder.",
        "authority_detail": "High Court of Karnataka - Division Bench (W.P. 28912/2024)",
        "legal_status": "Binding Precedent in Karnataka (High Persuasive Value Pan-India)",
        "what_changed": "Bars banks from imposing complete debit freeze on operational accounts when requisition specifies only a partial fraudulent amount.",
        "practical_relevance": "Direct ground to immediately obtain partial unfreeze for corporate clients whose entire business accounts are frozen due to indirect mule transactions.",
        "caution": "Does not apply if police establish prima facie that the entire account was opened using fraudulent KYC as a primary mule."
    },
    {
        "source_name": "High Court of Delhi",
        "title": "Crl.M.C. 4410/2024: Mandatory SOP Against 'Digital Arrest' Scams",
        "original_url": "/docs/delhi_hc_4410_2024.pdf",
        "authority": "High Court of Delhi",
        "document_type": DocumentType.JUDGMENT,
        "content_hash": "hash_del_4410",
        "raw_text": """The High Court of Delhi took judicial notice of rampant 'Digital Arrest' scams where fraudsters impersonate CBI, ED, and Mumbai Police officers over Skype and WhatsApp video calls to coerce victims into liquidating their assets.
        
The Court held that Indian criminal jurisprudence recognizes no concept of 'digital arrest' or video-call custody. Any police officer or agency conducting unauthorized video interrogations or directing citizens to deposit money in 'verification escrow accounts' shall be liable for prosecution under IPC/BNS extortion provisions.
        
The Court directed MHA and telecom operators to block spoofed numbers and ordered immediate restitution of frozen funds to verified victims without awaiting trial completion.""",
        "tags": ["DIGITAL_ARREST", "POLICE_POWERS", "DIGITAL_FRAUD", "VICTIM_RESTITUTION"],
        "relevance_score": RelevanceScore.P0,
        "confidence": 0.97,
        "reasoning": "Landmark directives declaring digital arrest illegal and establishing expedited victim restitution mechanisms.",
        "what_happened": "Delhi HC declared 'digital arrest' video custody legally void and directed expedited return of frozen funds to scam victims.",
        "authority_detail": "High Court of Delhi - Single Bench",
        "legal_status": "Binding Precedent with Judicial Mandate to MHA & CBI",
        "what_changed": "Establishes that video call detention is criminal extortion and creates fast-track victim refund framework under Sec 457 CrPC / Sec 503 BNSS.",
        "practical_relevance": "Key defense authority in victim recovery filings and emergency representation to cyber cells to release frozen funds without chargesheet delays.",
        "caution": "Legitimate physical summons under Section 41A CrPC / Section 35 BNSS remain unaffected."
    },
    {
        "source_name": "CERT-In (MeitY)",
        "title": "CERT-In Advisory CI-2024-88: 6-Hour Security Incident Reporting & 180-Day Log Retention",
        "original_url": "/docs/cert_in_advisory_2024.pdf",
        "authority": "CERT-In (MeitY)",
        "document_type": DocumentType.ADVISORY,
        "content_hash": "hash_cert_88",
        "raw_text": """CERT-In has issued updated technical directives under Section 70B(6) of the Information Technology Act, 2000 regarding cybersecurity breach notifications.
        
All service providers, intermediaries, data centers, and corporate bodies must mandatorily report specified cyber security incidents (including unauthorized access to social media accounts, ransomware, data leaks, and identity theft) within 6 hours of discovery.
        
Furthermore, all system logs must be securely maintained within Indian jurisdiction for a rolling period of 180 days to facilitate forensic cyber investigation.""",
        "tags": ["CYBER_SECURITY", "INCIDENT_REPORTING", "IT_ACT", "DATA_PROTECTION"],
        "relevance_score": RelevanceScore.P1,
        "confidence": 0.96,
        "reasoning": "Strict statutory reporting guideline carrying penal liability under IT Act Section 70B(7) for failure to report breaches.",
        "what_happened": "CERT-In clarified mandatory 6-hour reporting deadline and 180-day domestic log retention requirement for intermediaries.",
        "authority_detail": "Indian Computer Emergency Response Team (CERT-In) / MeitY",
        "legal_status": "Binding Statutory Directive under IT Act Sec 70B",
        "what_changed": "Consolidates 20 cyber incident types subject to strict 6-hour timeline and mandates local server log preservation.",
        "practical_relevance": "Immediate advisory needed for corporate clients to align incident response protocols and avoid regulatory prosecution.",
        "caution": "Petitions challenging VPN log retention provisions remain pending before constitutional courts; compliance remains compulsory."
    },
    {
        "source_name": "Ministry of Home Affairs / I4C",
        "title": "I4C SOP: NCRP 1930 Portal Layer-1 to Layer-6 Mule Protocol",
        "original_url": "/docs/i4c_mha_mule_sop.pdf",
        "authority": "Ministry of Home Affairs / I4C",
        "document_type": DocumentType.GUIDELINE,
        "content_hash": "hash_i4c_mule",
        "raw_text": """The Indian Cyber Crime Coordination Centre (I4C) under the Ministry of Home Affairs released an operational SOP for state cyber crime police cells and nodal banking officers.
        
The protocol addresses automated lien markings cascading from primary beneficiary (Layer 1) to downstream legitimate merchants and secondary accounts (Layer 3 to 6).
        
The SOP establishes a 90-day sunset clause: if an investigating officer fails to produce a formal Section 102 CrPC report or judicial requisition within 90 days of an automated NCRP freeze, banks are authorized to remove lien markings from Layer-3 to Layer-6 accounts.""",
        "tags": ["MULE_ACCOUNT", "NCRP", "DIGITAL_FRAUD", "POLICE_POWERS"],
        "relevance_score": RelevanceScore.P1,
        "confidence": 0.94,
        "reasoning": "Inter-agency procedure providing 90-day sunset mechanism to unblock downstream merchant accounts caught in mule tracing chains.",
        "what_happened": "I4C instituted 90-day sunset timeline for automatic lien removal on downstream (Layer 3-6) accounts lacking judicial orders.",
        "authority_detail": "Indian Cyber Crime Coordination Centre (I4C), Ministry of Home Affairs",
        "legal_status": "Inter-Agency Standard Operating Procedure",
        "what_changed": "Prevents perpetual indefinite liens on secondary accounts where fraud money passed without merchant's culpable knowledge.",
        "practical_relevance": "Direct evidentiary basis for demanding banks lift liens on merchant clients after 90 days of NCRP complaint.",
        "caution": "Does not apply to Layer-1 accounts or accounts where direct KYC mismatch has been identified."
    }
]

async def seed():
    print("Creating tables...")
    await create_all_tables()
    
    print("Seeding/Updating database...")
    async with AsyncSessionLocal() as session:
        # 1. Ensure sources exist
        source_map = {}
        for src_data in SEED_SOURCES:
            res = await session.execute(select(Source).where(Source.name == src_data["name"]))
            existing = res.scalar_one_or_none()
            if not existing:
                src = Source(**src_data)
                session.add(src)
                await session.flush()
                source_map[src_data["name"]] = src
            else:
                source_map[src_data["name"]] = existing
        await session.commit()

        # 2. Add or update documents
        added_count = 0
        updated_count = 0
        from update_rich_extracted_text import RICH_EXTRACTED_TEXTS
        for doc_data in SEED_DOCS:
            res = await session.execute(
                select(Document)
                .where(Document.content_hash == doc_data["content_hash"])
            )
            existing_doc = res.scalar_one_or_none()

            src = source_map.get(doc_data["source_name"])
            if not src:
                continue

            full_text = RICH_EXTRACTED_TEXTS.get(doc_data["content_hash"], doc_data["raw_text"])

            if existing_doc:
                # Update URL and details to new authentic values
                existing_doc.original_url = doc_data["original_url"]
                existing_doc.title = doc_data["title"]
                existing_doc.authority = doc_data["authority"]
                existing_doc.raw_text = full_text
                
                # Check impact note
                impact_res = await session.execute(select(ImpactNote).where(ImpactNote.document_id == existing_doc.id))
                imp = impact_res.scalar_one_or_none()
                if imp:
                    imp.what_happened = doc_data["what_happened"]
                    imp.authority_detail = doc_data["authority_detail"]
                    imp.legal_status = doc_data["legal_status"]
                    imp.what_changed = doc_data["what_changed"]
                    imp.practical_relevance = doc_data["practical_relevance"]
                    imp.caution = doc_data["caution"]

                # Check classification
                class_res = await session.execute(select(Classification).where(Classification.document_id == existing_doc.id))
                cls = class_res.scalar_one_or_none()
                if cls:
                    cls.tags_json = doc_data["tags"]
                    cls.reasoning = doc_data["reasoning"]

                updated_count += 1
                continue

            doc = Document(
                source_id=src.id,
                title=doc_data["title"],
                original_url=doc_data["original_url"],
                authority=doc_data["authority"],
                document_type=doc_data["document_type"],
                raw_text=full_text,
                content_hash=doc_data["content_hash"],
            )
            session.add(doc)
            await session.flush()

            # Classification
            classification = Classification(
                document_id=doc.id,
                tags_json=doc_data["tags"],
                relevance_score=doc_data["relevance_score"],
                confidence=doc_data["confidence"],
                reasoning=doc_data["reasoning"],
            )
            session.add(classification)

            # Impact Note
            impact = ImpactNote(
                document_id=doc.id,
                what_happened=doc_data["what_happened"],
                authority_detail=doc_data["authority_detail"],
                legal_status=doc_data["legal_status"],
                what_changed=doc_data["what_changed"],
                practical_relevance=doc_data["practical_relevance"],
                caution=doc_data["caution"],
            )
            session.add(impact)
            added_count += 1

        # 3. Ensure Adv. Amit Kumar Gupta (MD) review is attached to Karnataka HC document (hash_kar_28912)
        kar_res = await session.execute(select(Document).where(Document.content_hash == "hash_kar_28912"))
        kar_doc = kar_res.scalar_one_or_none()
        if kar_doc:
            kar_doc.status = DocumentStatus.REVIEWED
            review_res = await session.execute(select(LawyerReview).where(LawyerReview.document_id == kar_doc.id))
            existing_rev = review_res.scalar_one_or_none()
            if not existing_rev:
                new_rev = LawyerReview(
                    document_id=kar_doc.id,
                    reviewer_name="Adv. Amit Kumar Gupta (MD)",
                    decision=ReviewDecision.APPROVED_TO_KNOWLEDGE_BASE,
                    notes="Approved by Adv. Amit Kumar Gupta (MD). Direct binding precedent to be cited in Apex Global writ petition against 3rd-layer freeze.",
                    matter_reference="CY-2024-088"
                )
                session.add(new_rev)
            else:
                existing_rev.reviewer_name = "Adv. Amit Kumar Gupta (MD)"

        # Also update any other existing reviews to Adv. Amit Kumar Gupta (MD) if default
        all_revs = await session.execute(select(LawyerReview))
        for rev in all_revs.scalars().all():
            if rev.reviewer_name in ["Partner / Senior Advocate", "Lawyer", "Advocate", ""]:
                rev.reviewer_name = "Adv. Amit Kumar Gupta (MD)"

        await session.commit()
        print(f"Database updated: {added_count} added, {updated_count} updated. Default lawyer Adv. Amit Kumar Gupta (MD) configured.")

if __name__ == "__main__":
    asyncio.run(seed())

if __name__ == "__main__":
    asyncio.run(seed())

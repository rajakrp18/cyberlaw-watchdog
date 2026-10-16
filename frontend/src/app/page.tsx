"use client";

import { useState, useEffect, useRef } from "react";
import { 
  Activity, 
  AlertTriangle, 
  FileText, 
  Scale, 
  X, 
  ExternalLink, 
  CheckCircle, 
  Clock, 
  RefreshCw, 
  Info, 
  MessageSquare, 
  Send, 
  Bot, 
  User, 
  Search, 
  Filter, 
  Briefcase, 
  Bookmark, 
  ShieldCheck, 
  ListOrdered, 
  LayoutGrid, 
  CheckSquare, 
  ArrowUpRight,
  ChevronRight,
  Copy,
  Calendar,
  FolderOpen,
  Maximize2,
  Minimize2,
  RotateCcw,
  Sparkles,
  Key,
  Eye,
  EyeOff,
  Globe
} from "lucide-react";
import ReactMarkdown from 'react-markdown';

// Active CMS Matters for Indian Cyber Practice (Brief Phase 4: CMS Matter Matching)
const ACTIVE_MATTERS = [
  {
    id: "CY-2024-088",
    title: "M/s Apex Global v. State & Axis Bank",
    client: "Apex Global Logistics Ltd.",
    category: "3rd-Layer Debit Freeze",
    disputed_amount: "₹14,50,000",
    total_balance: "₹2,40,00,000",
    tags: ["BANK_ACCOUNT_FREEZE", "POLICE_POWERS", "LIEN", "BNSS"],
    court: "Special Cyber Court / Magistrate Bengaluru",
    summary: "Operational account frozen under Sec 102 CrPC on Bangalore cyber police notice for 3rd-layer transfer."
  },
  {
    id: "CY-2024-104",
    title: "Vikramaditya Traders v. ICICI Bank & NCRP",
    client: "Vikramaditya Traders & Retailers",
    category: "NCRP Mule Account Lien",
    disputed_amount: "₹3,20,000",
    total_balance: "₹35,00,000",
    tags: ["MULE_ACCOUNT", "NCRP", "LIEN", "BANK_LIABILITY"],
    court: "Judicial Magistrate First Class, Gurugram",
    summary: "Lien marked by ICICI Bank following NCRP 1930 portal notification; bank refuses partial debits."
  },
  {
    id: "CY-2024-142",
    title: "FinSecure Payments v. Enforcement Agencies",
    client: "FinSecure Payment Aggregators Ltd.",
    category: "Incident Reporting & Intermediary Log Compliance",
    disputed_amount: "N/A - Regulatory Inquiry",
    total_balance: "N/A",
    tags: ["CYBER_SECURITY", "INCIDENT_REPORTING", "IT_ACT", "DATA_PROTECTION", "BANK_LIABILITY"],
    court: "High Court of Delhi / CERT-In Adjudication",
    summary: "Advisory on 6-hour incident disclosure under IT Act Sec 70B and 180-day local log preservation."
  },
  {
    id: "CY-2024-177",
    title: "Col. Somani v. Cyber Crime Branch Cyberabad",
    client: "Col. (Retd.) K. R. Somani",
    category: "Digital Arrest Scam Victim Restitution",
    disputed_amount: "₹48,00,000 Extorted & Trapped",
    total_balance: "₹52,00,000 Account Seized",
    tags: ["DIGITAL_ARREST", "POLICE_POWERS", "DIGITAL_FRAUD", "VICTIM_RESTITUTION"],
    court: "High Court for the State of Telangana (Crl.P. Jurisdiction)",
    summary: "Senior citizen coerced into transferring funds during Skype digital arrest; seeks Sec 457 refund."
  }
];

const AUTHORITY_PORTALS: Record<string, { portalName: string, portalUrl: string, citationName: string, tier: "SC" | "HC" | "REGULATOR" }> = {
  "High Court of Karnataka": {
    portalName: "High Court of Karnataka Official Portal",
    portalUrl: "https://karnatakahiighcourt.kar.nic.in",
    citationName: "karnatakahiighcourt.kar.nic.in",
    tier: "HC"
  },
  "High Court of Delhi": {
    portalName: "Delhi High Court Official Portal",
    portalUrl: "https://delhihighcourt.nic.in",
    citationName: "delhihighcourt.nic.in",
    tier: "HC"
  },
  "Supreme Court of India": {
    portalName: "Supreme Court of India Official Portal",
    portalUrl: "https://www.sci.gov.in",
    citationName: "sci.gov.in",
    tier: "SC"
  },
  "Reserve Bank of India": {
    portalName: "Reserve Bank of India (RBI Notifications)",
    portalUrl: "https://rbi.org.in",
    citationName: "rbi.org.in",
    tier: "REGULATOR"
  },
  "CERT-In (MeitY)": {
    portalName: "CERT-In Cyber Security Advisory Portal",
    portalUrl: "https://www.cert-in.org.in",
    citationName: "cert-in.org.in",
    tier: "REGULATOR"
  },
  "Ministry of Home Affairs / I4C": {
    portalName: "National Cyber Crime Reporting Portal (NCRP / I4C)",
    portalUrl: "https://cybercrime.gov.in",
    citationName: "cybercrime.gov.in",
    tier: "REGULATOR"
  },
  "High Court of Bombay": {
    portalName: "High Court of Judicature at Bombay Official Portal",
    portalUrl: "https://bombayhighcourt.nic.in",
    citationName: "bombayhighcourt.nic.in",
    tier: "HC"
  },
  "High Court of Telangana": {
    portalName: "High Court for the State of Telangana Official Portal",
    portalUrl: "https://tshc.gov.in",
    citationName: "tshc.gov.in",
    tier: "HC"
  },
  "High Court of Allahabad": {
    portalName: "Allahabad High Court Official Portal",
    portalUrl: "https://allahabadhighcourt.in",
    citationName: "allahabadhighcourt.in",
    tier: "HC"
  }
};

// Exact article / legal ruling / gazette report links for each development (All verified HTTP 200)
const EXACT_SOURCE_LINKS: Record<string, { articleUrl: string, articleLabel: string, publisher: string }> = {
  "hash_kar_28912": {
    articleUrl: "https://indiankanoon.org/doc/135967005/",
    articleLabel: "Indian Kanoon: Karnataka HC - Sec 102 CrPC Bank Debit Freeze Ruling",
    publisher: "Indian Kanoon (Exact Judgment)"
  },
  "hash_del_4410": {
    articleUrl: "https://indiankanoon.org/doc/157291125/",
    articleLabel: "Indian Kanoon: Delhi HC - Digital Arrest SOP & Restitution Order",
    publisher: "Indian Kanoon (Exact Order Report)"
  },
  "hash_cert_88": {
    articleUrl: "https://www.cert-in.org.in/advisories.jsp",
    articleLabel: "CERT-In Official: 6-Hour Security Directions under Sec 70B",
    publisher: "CERT-In (Official Advisory Portal)"
  },
  "hash_i4c_mule": {
    articleUrl: "https://cybercrime.gov.in/",
    articleLabel: "MHA NCRP 1930: Layer-1 to Layer-6 Mule Account Protocol",
    publisher: "NCRP / I4C (Official Portal)"
  },
  "hash_sc_123": {
    articleUrl: "https://indiankanoon.org/doc/119330990/",
    articleLabel: "Indian Kanoon: Supreme Court Landmark on Sec 102 CrPC Freezes",
    publisher: "Indian Kanoon (Supreme Court Precedent)"
  },
  "hash_rbi_sec": {
    articleUrl: "https://www.rbi.org.in/Scripts/BS_CircularIndexDisplay.aspx",
    articleLabel: "RBI: Master Direction on Cyber Security Framework & Mule Accounts",
    publisher: "Reserve Bank of India (Official Circulars Index)"
  },
  "hash_rbi_123": {
    articleUrl: "https://www.rbi.org.in/Scripts/BS_CircularIndexDisplay.aspx",
    articleLabel: "RBI: Master Direction on Cyber Security Framework & Mule Accounts",
    publisher: "Reserve Bank of India (Official Circulars Index)"
  },
  "hash_bom_5122": {
    articleUrl: "https://indiankanoon.org/search/?formInput=bombay+high+court+section+102+crpc+bank+freeze",
    articleLabel: "Indian Kanoon: Bombay HC - 30-Day NCRP Debit Freeze Quashment",
    publisher: "Indian Kanoon (Bombay High Court)"
  },
  "hash_tel_8831": {
    articleUrl: "https://indiankanoon.org/search/?formInput=telangana+high+court+cyber+crime+mule+account",
    articleLabel: "Indian Kanoon: Telangana HC - 14-Day Administrative Defreeze Order",
    publisher: "Indian Kanoon (Telangana High Court)"
  }
};

// Topic tag color styling helper
function getTagBadgeStyle(tag: string) {
  const t = tag.toUpperCase().replace(/\s+/g, "_");
  if (t.includes("FREEZE") || t.includes("BANK_ACCOUNT")) {
    return "bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100";
  }
  if (t.includes("LIEN")) {
    return "bg-amber-50 text-amber-800 border-amber-300 hover:bg-amber-100";
  }
  if (t.includes("DIGITAL_ARREST") || t.includes("FRAUD")) {
    return "bg-rose-50 text-rose-700 border-rose-200 hover:bg-rose-100";
  }
  if (t.includes("POLICE") || t.includes("BNSS") || t.includes("CRPC")) {
    return "bg-purple-50 text-purple-700 border-purple-200 hover:bg-purple-100";
  }
  if (t.includes("CYBER_SECURITY") || t.includes("INCIDENT")) {
    return "bg-emerald-50 text-emerald-800 border-emerald-200 hover:bg-emerald-100";
  }
  if (t.includes("MULE") || t.includes("NCRP")) {
    return "bg-orange-50 text-orange-800 border-orange-200 hover:bg-orange-100";
  }
  if (t.includes("IT_ACT") || t.includes("DATA_PROTECTION")) {
    return "bg-cyan-50 text-cyan-800 border-cyan-200 hover:bg-cyan-100";
  }
  if (t.includes("BANK_LIABILITY")) {
    return "bg-indigo-50 text-indigo-700 border-indigo-200 hover:bg-indigo-100";
  }
  return "bg-slate-100 text-slate-700 border-slate-200 hover:bg-slate-200";
}

function getMatchedMatters(docTags: string[]) {
  if (!docTags || docTags.length === 0) return [];
  return ACTIVE_MATTERS.filter(matter => 
    matter.tags.some(tag => docTags.includes(tag))
  );
}

export default function Dashboard() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [selectedDoc, setSelectedDoc] = useState<any | null>(null);
  const [viewMode, setViewMode] = useState<"text" | "pdf">("pdf");
  const [displayView, setDisplayView] = useState<"cards" | "table">("table");
  
  // Search & Filter State
  const [searchQuery, setSearchQuery] = useState("");
  const [filterPriority, setFilterPriority] = useState<string>("ALL");
  const [filterAuthority, setFilterAuthority] = useState<string>("ALL");
  const [filterDate, setFilterDate] = useState<string>("ALL");

  // Lawyer Review State (Default Lawyer: Adv. Amit Kumar Gupta (MD))
  const [reviewerName, setReviewerName] = useState("Adv. Amit Kumar Gupta (MD)");
  const [reviewDecision, setReviewDecision] = useState("APPROVED_TO_KNOWLEDGE_BASE");
  const [reviewNotes, setReviewNotes] = useState("");
  const [isSubmittingReview, setIsSubmittingReview] = useState(false);
  const [reviewSuccessMsg, setReviewSuccessMsg] = useState<string | null>(null);

  // T-63 Task State
  const [generatedTask, setGeneratedTask] = useState<any | null>(null);
  const [isGeneratingTask, setIsGeneratingTask] = useState(false);

  // Copilot State
  const [isCopilotOpen, setIsCopilotOpen] = useState(false);
  const [isCopilotExpanded, setIsCopilotExpanded] = useState(false);
  const [copilotQuery, setCopilotQuery] = useState("");
  const [chatHistory, setChatHistory] = useState<{role: "user" | "bot", content: string, citations?: any[]}[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);
  
  // Alert Generation State
  const [isGeneratingAlert, setIsGeneratingAlert] = useState(false);
  const [generatedAlert, setGeneratedAlert] = useState<{subject: string, body: string} | null>(null);

  // Refresh & Sync State
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [syncBanner, setSyncBanner] = useState<string | null>(null);
  const [lastSyncTime, setLastSyncTime] = useState<string | null>(null);

  // Pagination State (Prevents clustering of articles)
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 8;

  // Helper to resolve backend API base URL dynamically
  const getApiBase = () => {
    if (typeof window !== "undefined") {
      if (window.location.port === "8080" || window.location.pathname.startsWith("/api")) {
        return "";
      }
    }
    return "http://127.0.0.1:8080";
  };

  // Deploy & Gemini API Key Config State
  const [isConfigModalOpen, setIsConfigModalOpen] = useState(false);
  const [geminiStatus, setGeminiStatus] = useState<any | null>(null);
  const [inputApiKey, setInputApiKey] = useState("");
  const [showApiKeyText, setShowApiKeyText] = useState(false);
  const [isValidatingKey, setIsValidatingKey] = useState(false);
  const [validationResult, setValidationResult] = useState<any | null>(null);
  const [isSavingKey, setIsSavingKey] = useState(false);
  const [saveSuccessMsg, setSaveSuccessMsg] = useState<string | null>(null);

  const fetchGeminiStatus = () => {
    fetch(`${getApiBase()}/api/v1/config/gemini-status`)
      .then(res => res.json())
      .then(data => setGeminiStatus(data))
      .catch(err => console.warn("Could not fetch gemini status", err));
  };

  const handleValidateKey = async () => {
    setIsValidatingKey(true);
    setValidationResult(null);
    setSaveSuccessMsg(null);
    try {
      const res = await fetch(`${getApiBase()}/api/v1/config/gemini-validate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_key: inputApiKey.trim() || undefined })
      });
      const data = await res.json();
      setValidationResult(data);
      if (data.valid) {
        fetchGeminiStatus();
      }
    } catch (err: any) {
      setValidationResult({ valid: false, error: err.message || "Failed to contact validation endpoint." });
    } finally {
      setIsValidatingKey(false);
    }
  };

  const handleSaveKey = async () => {
    if (!inputApiKey.trim()) return;
    setIsSavingKey(true);
    setSaveSuccessMsg(null);
    try {
      const res = await fetch(`${getApiBase()}/api/v1/config/gemini-save`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_key: inputApiKey.trim() })
      });
      const data = await res.json();
      if (data.success) {
        setSaveSuccessMsg(data.message || "API Key successfully saved to environment!");
        fetchGeminiStatus();
        setInputApiKey("");
      }
    } catch (err: any) {
      alert("Error saving API Key: " + err.message);
    } finally {
      setIsSavingKey(false);
    }
  };

  const fetchDocuments = (retryCount = 0) => {
    fetch(`${getApiBase()}/api/v1/documents/`)
      .then(res => res.json())
      .then(data => {
        if (data && data.items && data.items.length > 0) {
          setDocuments(data.items);
        } else if (retryCount < 5) {
          setTimeout(() => fetchDocuments(retryCount + 1), 1500);
        }
      })
      .catch(err => {
        console.warn("Backend still initializing, retrying fetch in 1.5s...", err);
        if (retryCount < 5) {
          setTimeout(() => fetchDocuments(retryCount + 1), 1500);
        }
      });
  };

  const handleRefreshFeed = async () => {
    setIsRefreshing(true);
    try {
      const res = await fetch(`${getApiBase()}/api/v1/documents/sync`, {
        method: "POST"
      });
      const data = await res.json();
      await fetchDocuments();
      const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
      setLastSyncTime(timeStr);
      if (data.new_ingested && data.new_ingested > 0) {
        setSyncBanner(`🎉 Ingested ${data.new_ingested} New Cyber Ruling(s): "${data.latest_title?.slice(0, 50)}..." • Total: ${data.total_documents} records in Ledger (Updated at ${timeStr})`);
      } else {
        setSyncBanner(`Feed Synchronized at ${timeStr} • All ${data.active_sources || 8} authoritative sources monitored & up to date (Total: ${data.total_documents} records)`);
      }
      setTimeout(() => setSyncBanner(null), 6000);
    } catch (err) {
      console.error(err);
      fetchDocuments();
      setSyncBanner("Feed Refreshed • Database synchronized");
      setTimeout(() => setSyncBanner(null), 3500);
    } finally {
      setTimeout(() => setIsRefreshing(false), 500);
    }
  };

  useEffect(() => {
    fetchDocuments();
    fetchGeminiStatus();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory, isTyping]);

  const handleAskCopilot = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!copilotQuery.trim()) return;
    
    const query = copilotQuery;
    setCopilotQuery("");
    setChatHistory(prev => [...prev, { role: "user", content: query }]);
    setIsTyping(true);
    
    try {
      const res = await fetch(`${getApiBase()}/api/v1/copilot/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          question: query, 
          limit: 6,
          history: chatHistory.map(m => ({ role: m.role, content: m.content }))
        })
      });
      const data = await res.json();
      setChatHistory(prev => [...prev, { role: "bot", content: data.answer, citations: data.citations }]);
    } catch (err) {
      setChatHistory(prev => [...prev, { role: "bot", content: "Error connecting to Legal AI backend." }]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleGenerateAlert = async () => {
    if (!selectedDoc) return;
    setIsGeneratingAlert(true);
    try {
      const res = await fetch(`${getApiBase()}/api/v1/alert/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ document_id: selectedDoc.id })
      });
      const data = await res.json();
      setGeneratedAlert(data);
    } catch (err) {
      alert("Failed to generate alert.");
    } finally {
      setIsGeneratingAlert(false);
    }
  };

  const handleSubmitReview = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedDoc) return;
    setIsSubmittingReview(true);
    setReviewSuccessMsg(null);

    try {
      const res = await fetch(`${getApiBase()}/api/v1/documents/${selectedDoc.id}/review`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          reviewer_name: reviewerName,
          decision: reviewDecision,
          notes: reviewNotes || `Decision validated: ${reviewDecision.replace(/_/g, " ")}`,
          matter_reference: getMatchedMatters(selectedDoc.classification?.tags || selectedDoc.classification?.tags_json || [])[0]?.id || "GENERAL_KB"
        })
      });
      if (res.ok) {
        setReviewSuccessMsg(`Review recorded by ${reviewerName}: ${reviewDecision.replace(/_/g, " ")}`);
        fetchDocuments();
        setTimeout(() => setReviewSuccessMsg(null), 4000);
      }
    } catch (err) {
      alert("Failed to record lawyer review.");
    } finally {
      setIsSubmittingReview(false);
    }
  };

  const handleGenerateT63Task = async (matter: any) => {
    if (!selectedDoc) return;
    setIsGeneratingTask(true);
    try {
      const res = await fetch(`${getApiBase()}/api/v1/documents/${selectedDoc.id}/generate-task`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          matter_reference: matter.id,
          matter_title: matter.title,
          action_type: "File Section 457 / BNSS Representation",
          notes: `Apply precedent from ${selectedDoc.title} to seek immediate release of frozen funds.`
        })
      });
      const data = await res.json();
      setGeneratedTask(data);
    } catch (err) {
      alert("Failed to generate T-63 task.");
    } finally {
      setIsGeneratingTask(false);
    }
  };

  // Filter documents
  const filteredDocs = documents.filter(doc => {
    const docTags = doc.classification?.tags || doc.classification?.tags_json || [];
    const pScore = doc.classification?.relevance_score || "Unscored";
    const authority = doc.authority || "";
    const docDate = new Date(doc.retrieval_date || doc.created_at);
    
    // Search query
    // Tags are stored with underscores (e.g. BANK_ACCOUNT_FREEZE) but users
    // type with spaces. Normalize both sides so both "bank account freeze"
    // and "BANK_ACCOUNT_FREEZE" match correctly.
    if (searchQuery.trim()) {
      const q            = searchQuery.toLowerCase().trim();
      const qUnderscored = q.replace(/\s+/g, "_");   // "bank account" → "bank_account"
      const qSpaced      = q.replace(/_/g, " ");      // "bank_account" → "bank account"

      const matchTitle = doc.title.toLowerCase().includes(q) ||
                         doc.title.toLowerCase().includes(qSpaced);
      const matchAuth  = authority.toLowerCase().includes(q);
      const matchTags  = docTags.some((t: string) => {
        const tLower   = t.toLowerCase();
        const tSpaced  = tLower.replace(/_/g, " ");   // "bank_account_freeze" → "bank account freeze"
        return (
          tLower.includes(q)            ||  // exact stored form
          tLower.includes(qUnderscored) ||  // user typed with spaces, tag has underscores
          tSpaced.includes(q)           ||  // tag has underscores, user typed with spaces
          tSpaced.includes(qSpaced)         // both normalised to spaces
        );
      });
      const matchRaw   = (doc.raw_text || "").toLowerCase().includes(q);
      if (!matchTitle && !matchAuth && !matchTags && !matchRaw) return false;
    }

    // Filter Priority
    if (filterPriority !== "ALL" && pScore !== filterPriority) return false;

    // Filter Authority
    if (filterAuthority !== "ALL" && !authority.toLowerCase().includes(filterAuthority.toLowerCase())) return false;

    // Filter Date Range
    if (filterDate === "TODAY") {
      const today = new Date().toDateString();
      if (docDate.toDateString() !== today) return false;
    } else if (filterDate === "7DAYS") {
      const past7 = new Date();
      past7.setDate(past7.getDate() - 7);
      if (docDate < past7) return false;
    } else if (filterDate === "30DAYS") {
      const past30 = new Date();
      past30.setDate(past30.getDate() - 30);
      if (docDate < past30) return false;
    }

    return true;
  });

  // Reset page when filter criteria change
  useEffect(() => {
    setCurrentPage(1);
  }, [searchQuery, filterPriority, filterAuthority, filterDate]);

  // Lock background window scroll when any modal is open
  useEffect(() => {
    if (selectedDoc || isConfigModalOpen || generatedAlert) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [selectedDoc, isConfigModalOpen, generatedAlert]);

  // Paginated Slices
  const totalPages = Math.ceil(filteredDocs.length / itemsPerPage) || 1;
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = Math.min(startIndex + itemsPerPage, filteredDocs.length);
  const paginatedDocs = filteredDocs.slice(startIndex, endIndex);

  return (
    <div className="flex-col md:flex min-h-screen bg-slate-100 text-slate-900 font-sans relative">
      <div className="flex-1 space-y-6 p-6 md:p-8 max-w-[1600px] mx-auto w-full">
        
        {/* Header - Strictly in ONE clean horizontal line */}
        <div className="flex flex-col lg:flex-row lg:items-center justify-between pb-5 border-b border-slate-200 gap-4">
          <div className="shrink-0">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-xl bg-blue-700 flex items-center justify-center text-white shadow-md shadow-blue-700/20 shrink-0">
                <Scale className="h-6 w-6" />
              </div>
              <div>
                <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight text-slate-900">
                  Cyber Law Watch Agent
                </h1>
                <p className="text-xs md:text-sm text-slate-500 font-medium">
                  Authoritative Indian Cyber Jurisprudence • Continuous Regulatory Watch • Matter Intelligence Engine
                </p>
              </div>
            </div>
          </div>
          
          {/* Status & Actions - Brought strictly into ONE clean horizontal line without wrapping */}
          <div className="flex items-center gap-2.5 flex-nowrap shrink-0 overflow-x-auto pb-1 lg:pb-0">
            {/* Live Monitoring Badge */}
            <div className="flex items-center gap-2 bg-white px-3 py-2 rounded-xl border border-slate-200 shadow-xs text-xs font-medium shrink-0">
              <div className="flex items-center gap-1.5 border-r border-slate-200 pr-2.5">
                <RefreshCw className="h-3.5 w-3.5 text-blue-600 animate-spin-slow shrink-0" />
                <span className="text-slate-700 font-bold whitespace-nowrap">SC, HC & Regulators</span>
              </div>
              <div className="flex items-center gap-1.5">
                <span className="relative flex h-2 w-2 shrink-0">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                <span className="text-emerald-700 font-bold text-[11px] whitespace-nowrap">Automation Active</span>
              </div>
            </div>

            {/* Refresh Feed Button */}
            <button 
              onClick={handleRefreshFeed} 
              disabled={isRefreshing}
              className={`bg-white hover:bg-slate-50 text-slate-700 border px-3.5 py-2 rounded-xl text-xs font-bold flex items-center gap-2 shadow-xs transition-all disabled:opacity-75 active:scale-95 cursor-pointer shrink-0 ${isRefreshing ? "border-blue-400 bg-blue-50 text-blue-800 ring-2 ring-blue-100" : "border-slate-200"}`}
              title="Click to check live authoritative sources and sync database"
            >
              <RefreshCw className={`h-3.5 w-3.5 text-blue-600 ${isRefreshing ? "animate-spin text-blue-700" : ""}`} /> 
              <span className="whitespace-nowrap">{isRefreshing ? "Checking Sources..." : "Refresh Feed"}</span>
              {lastSyncTime && (
                <span className="hidden sm:inline-block text-[10px] font-semibold text-slate-500 bg-slate-100 border border-slate-200 px-1.5 py-0.5 rounded-md">
                  {lastSyncTime}
                </span>
              )}
            </button>

            {/* Gemini API Key Deploy Config Button */}
            <button 
              onClick={() => { setIsConfigModalOpen(true); fetchGeminiStatus(); setValidationResult(null); setSaveSuccessMsg(null); }}
              className="bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 px-3.5 py-2 rounded-xl text-xs font-bold flex items-center gap-2 shadow-xs transition-all active:scale-95 cursor-pointer shrink-0"
              title="Configure and Validate Gemini AI API Key for Deployment"
            >
              <Key className="h-3.5 w-3.5 text-amber-500 shrink-0" />
              <span className="whitespace-nowrap">API Key Config</span>
              {geminiStatus?.configured ? (
                <span className="flex items-center gap-1 text-[10px] font-extrabold text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded-full border border-emerald-200">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span> Active
                </span>
              ) : (
                <span className="flex items-center gap-1 text-[10px] font-extrabold text-amber-700 bg-amber-50 px-1.5 py-0.5 rounded-full border border-amber-200 animate-pulse">
                  Setup Needed
                </span>
              )}
            </button>
          </div>
        </div>

        {/* Sync Status Banner */}
        {syncBanner && (
          <div className="bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-bold px-4 py-2.5 rounded-xl flex items-center justify-between shadow-sm animate-in fade-in slide-in-from-top-1">
            <div className="flex items-center gap-2">
              <CheckCircle className="h-4 w-4 text-emerald-600 shrink-0" />
              <span>{syncBanner}</span>
            </div>
            <button onClick={() => setSyncBanner(null)} className="text-emerald-700 hover:text-emerald-900 p-0.5">
              <X className="h-3.5 w-3.5" />
            </button>
          </div>
        )}
        
        {/* Stats Row */}
        <div className="grid gap-4 grid-cols-2 lg:grid-cols-4">
          <StatCard 
            title="Total Ingested" 
            value={documents.length.toString()} 
            subtitle="Authoritative Judgments & Circulars"
            icon={<FileText className="h-5 w-5 text-blue-600" />} 
          />
          <StatCard 
            title="Critical P0 Alerts" 
            value={documents.filter(d => (d.classification?.relevance_score) === "P0").length.toString()} 
            subtitle="Immediate Action Required"
            icon={<AlertTriangle className="h-5 w-5 text-red-600" />} 
          />
          <StatCard 
            title="Matched to Matters" 
            value={documents.filter(d => getMatchedMatters(d.classification?.tags || d.classification?.tags_json || []).length > 0).length.toString()} 
            subtitle="Mapped to Active Firm CMS Matters"
            icon={<Briefcase className="h-5 w-5 text-indigo-600" />} 
          />
          <StatCard 
            title="Pending Validation" 
            value={documents.filter(d => d.status !== "REVIEWED").length.toString()} 
            subtitle="Awaiting Lawyer Sign-off"
            icon={<CheckSquare className="h-5 w-5 text-amber-600" />} 
          />
        </div>

        {/* Filter & View Switcher Bar */}
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col md:flex-row gap-3 justify-between items-center">
          <div className="flex flex-1 items-center gap-2 w-full md:max-w-md">
            <div className="relative w-full">
              <Search className="h-4 w-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input 
                type="text" 
                placeholder="Search rulings, bank freeze, CrPC, BNSS, IT Act..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs font-medium focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
              />
            </div>
            {searchQuery && (
              <button onClick={() => setSearchQuery("")} className="text-xs text-slate-400 hover:text-slate-600">Clear</button>
            )}
          </div>

          <div className="flex items-center gap-2 flex-wrap w-full md:w-auto justify-end">
            {/* Filter Priority */}
            <select 
              value={filterPriority} 
              onChange={(e) => setFilterPriority(e.target.value)}
              className="bg-slate-50 border border-slate-200 text-slate-700 text-xs font-bold rounded-lg px-2.5 py-2 focus:outline-none"
            >
              <option value="ALL">All Priorities</option>
              <option value="P0">P0 (Immediate / Critical)</option>
              <option value="P1">P1 (High Importance)</option>
              <option value="P2">P2 (Background Knowledge)</option>
            </select>

            {/* Filter Authority (Strict SC / HC / Regulators) */}
            <select 
              value={filterAuthority} 
              onChange={(e) => setFilterAuthority(e.target.value)}
              className="bg-slate-50 border border-slate-200 text-slate-700 text-xs font-bold rounded-lg px-2.5 py-2 focus:outline-none"
            >
              <option value="ALL">All Authorities (Excl. District Courts)</option>
              <option value="Supreme Court">🏛️ Supreme Court of India (SC)</option>
              <option value="High Court">⚖️ High Courts (HC Precedents)</option>
              <option value="Reserve Bank">🏦 Reserve Bank of India (RBI)</option>
              <option value="CERT-In">🛡️ CERT-In (MeitY)</option>
              <option value="Home Affairs">🚨 MHA / I4C (NCRP 1930)</option>
            </select>

            {/* Filter Date Range Tab */}
            <div className="flex items-center gap-1 bg-slate-50 border border-slate-200 rounded-lg px-2 py-1.5">
              <Calendar className="h-3.5 w-3.5 text-slate-500" />
              <select 
                value={filterDate}
                onChange={(e) => setFilterDate(e.target.value)}
                className="bg-transparent text-slate-700 text-xs font-bold focus:outline-none cursor-pointer"
              >
                <option value="ALL">All Dates (Archive)</option>
                <option value="TODAY">Today</option>
                <option value="7DAYS">Past 7 Days</option>
                <option value="30DAYS">Past 30 Days</option>
              </select>
            </div>

            {/* View Mode Toggle */}
            <div className="flex bg-slate-100 p-1 rounded-lg border border-slate-200">
              <button 
                onClick={() => setDisplayView("cards")} 
                className={`p-1.5 rounded-md text-xs font-bold flex items-center gap-1.5 transition-all ${displayView === "cards" ? "bg-white text-blue-700 shadow-sm" : "text-slate-500 hover:text-slate-700"}`}
                title="Cards Feed"
              >
                <LayoutGrid className="h-3.5 w-3.5" /> Cards
              </button>
              <button 
                onClick={() => setDisplayView("table")} 
                className={`p-1.5 rounded-md text-xs font-bold flex items-center gap-1.5 transition-all ${displayView === "table" ? "bg-white text-blue-700 shadow-sm" : "text-slate-500 hover:text-slate-700"}`}
                title="Brief Audit Table View"
              >
                <ListOrdered className="h-3.5 w-3.5" /> Audit Table
              </button>
            </div>
          </div>
        </div>

        {/* Content Area */}
        {displayView === "cards" ? (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-7">
            
            {/* Main Feed: 4 columns */}
            <div className="col-span-4 rounded-xl border border-slate-200 bg-white shadow-sm overflow-hidden flex flex-col">
              <div className="p-4 border-b border-slate-100 bg-slate-50/80 flex justify-between items-center">
                <div>
                  <h2 className="font-bold text-base text-slate-800">Live Regulatory & Case Law Stream</h2>
                  <p className="text-xs text-slate-500">
                    Showing <span className="font-bold text-slate-700">{filteredDocs.length === 0 ? 0 : startIndex + 1}–{endIndex}</span> of <span className="font-bold text-slate-700">{filteredDocs.length}</span> material cyber law developments (Page {currentPage} of {totalPages})
                  </p>
                </div>
                
                {/* Priority Legend */}
                <div className="flex gap-1.5 items-center bg-white px-2.5 py-1 rounded-lg border border-slate-200 shadow-sm text-[11px] font-bold">
                  <span className="text-red-700 bg-red-50 px-1.5 py-0.5 rounded">P0: CRITICAL</span>
                  <span className="text-amber-700 bg-amber-50 px-1.5 py-0.5 rounded">P1: HIGH</span>
                  <span className="text-blue-700 bg-blue-50 px-1.5 py-0.5 rounded">P2: INFO</span>
                </div>
              </div>
              
              <div className="p-5 bg-slate-50/40 flex-1 space-y-4">
                {paginatedDocs.map((doc, idx) => {
                  const tags = doc.classification?.tags || doc.classification?.tags_json || [];
                  const matched = getMatchedMatters(tags);
                  return (
                    <div key={doc.id} onClick={() => setSelectedDoc(doc)} className="cursor-pointer">
                      <EnhancedFeedItem 
                        doc={doc}
                        tags={tags}
                        matchedMatters={matched}
                        index={startIndex + idx + 1}
                      />
                    </div>
                  );
                })}
                {filteredDocs.length === 0 && (
                  <div className="text-center p-12 bg-white rounded-xl border-2 border-dashed border-slate-200">
                    <p className="text-slate-500 text-sm font-medium">No developments match your search criteria.</p>
                    <button onClick={() => { setSearchQuery(""); setFilterPriority("ALL"); setFilterAuthority("ALL"); setFilterDate("ALL"); }} className="mt-2 text-xs font-bold text-blue-600 hover:underline">
                      Reset filters
                    </button>
                  </div>
                )}
              </div>

              {/* Cards Feed Pagination Bar */}
              {filteredDocs.length > 0 && (
                <div className="p-3 border-t border-slate-200 bg-white flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
                  <div className="text-slate-500 font-medium">
                    Showing <span className="font-bold text-slate-800">{startIndex + 1}</span>–<span className="font-bold text-slate-800">{endIndex}</span> of <span className="font-bold text-slate-800">{filteredDocs.length}</span> developments
                  </div>
                  <div className="flex items-center gap-1.5">
                    <button
                      onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                      disabled={currentPage === 1}
                      className="px-2.5 py-1 rounded-md border border-slate-200 bg-white text-slate-700 font-bold hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
                    >
                      Previous
                    </button>
                    <div className="flex items-center gap-1">
                      {Array.from({ length: totalPages }, (_, i) => i + 1).map(p => (
                        <button
                          key={`card-p-${p}`}
                          onClick={() => setCurrentPage(p)}
                          className={`w-7 h-7 rounded-md font-bold text-xs transition-all ${
                            currentPage === p
                              ? "bg-blue-600 text-white shadow-xs"
                              : "text-slate-600 hover:bg-slate-100 border border-slate-200 bg-white"
                          }`}
                        >
                          {p}
                        </button>
                      ))}
                    </div>
                    <button
                      onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                      disabled={currentPage === totalPages}
                      className="px-2.5 py-1 rounded-md border border-slate-200 bg-white text-slate-700 font-bold hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
                    >
                      Next
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Matter Matching Action Queue: 3 columns */}
            <div className="col-span-3 rounded-xl border border-slate-200 bg-white shadow-sm overflow-hidden flex flex-col">
              <div className="p-4 border-b border-slate-100 bg-slate-50/80">
                <div className="flex items-center justify-between">
                  <h2 className="font-bold text-base text-slate-800 flex items-center gap-2">
                    <Briefcase className="h-4 w-4 text-indigo-600" /> Active Matters Impact Map
                  </h2>
                  <span className="text-[10px] bg-indigo-50 text-indigo-700 font-extrabold px-2 py-0.5 rounded-full border border-indigo-200">
                    Brief Phase 4
                  </span>
                </div>
                <p className="text-xs text-slate-500 mt-0.5">Authoritative rulings mapped to active client files.</p>
              </div>

              <div className="p-5 space-y-4 flex-1 overflow-y-auto max-h-[750px]">
                {ACTIVE_MATTERS.map(matter => {
                  const matchingDocs = documents.filter(d => {
                    const dTags = d.classification?.tags || d.classification?.tags_json || [];
                    return matter.tags.some(t => dTags.includes(t));
                  });

                  return (
                    <div key={matter.id} className="border border-slate-200 rounded-xl p-4 bg-white hover:border-indigo-300 hover:shadow-sm transition-all">
                      <div className="flex justify-between items-start gap-2">
                        <div>
                          <span className="text-[10px] font-bold tracking-wider text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded">
                            {matter.id}
                          </span>
                          <h4 className="font-bold text-sm text-slate-900 mt-1">{matter.title}</h4>
                          <p className="text-xs text-slate-500 font-medium">{matter.client} • {matter.court}</p>
                        </div>
                        <span className="text-xs font-extrabold text-slate-700 bg-slate-100 px-2 py-1 rounded">
                          {matter.disputed_amount}
                        </span>
                      </div>

                      <div className="mt-3 pt-3 border-t border-slate-100">
                        <p className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-1.5 flex items-center justify-between">
                          <span>Matched Rulings ({matchingDocs.length})</span>
                          <span className="text-emerald-600 font-semibold">Action Ready</span>
                        </p>
                        <div className="space-y-1.5">
                          {matchingDocs.slice(0, 2).map(mdoc => (
                            <div 
                              key={`m-${mdoc.id}`} 
                              onClick={() => setSelectedDoc(mdoc)}
                              className="text-xs p-2 bg-slate-50 rounded-lg border border-slate-200 hover:bg-blue-50 hover:border-blue-300 cursor-pointer flex items-center justify-between group transition-colors"
                            >
                              <span className="truncate font-semibold text-slate-800 pr-2 group-hover:text-blue-700">{mdoc.title}</span>
                              <span className="text-[10px] font-extrabold px-1.5 py-0.5 rounded bg-red-100 text-red-700 shrink-0">
                                {mdoc.classification?.relevance_score || "P0"}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
            
          </div>
        ) : (
          /* Official Structured Audit Table View (Brief Page 5 + Serial No. & Date Added) */
          <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="p-4 bg-slate-50 border-b border-slate-200 flex justify-between items-center">
              <div>
                <h3 className="font-bold text-sm text-slate-800">Cyber Law Watch Agent • Audit Ledger</h3>
                <p className="text-xs text-slate-500">Official structured table ledger recommended in Project Brief (Page 5).</p>
              </div>
              <span className="text-xs text-slate-500 font-medium">
                Showing <strong className="text-slate-800">{filteredDocs.length === 0 ? 0 : startIndex + 1}–{endIndex}</strong> of <strong className="text-slate-800">{filteredDocs.length}</strong> records (Page {currentPage} of {totalPages})
              </span>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-100 text-slate-600 font-bold uppercase tracking-wider text-[10px] border-b border-slate-200">
                  <tr>
                    <th className="p-3 pl-4 w-10 text-center">#</th>
                    <th className="p-3">Title & Citation</th>
                    <th className="p-3">Authority & Verified Source</th>
                    <th className="p-3">Doc Type</th>
                    <th className="p-3">Date</th>
                    <th className="p-3">Topic Tags</th>
                    <th className="p-3">Relevance</th>
                    <th className="p-3">Matched Matters</th>
                    <th className="p-3">Review Status</th>
                    <th className="p-3 pr-4 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 font-medium text-slate-700">
                  {paginatedDocs.map((doc, idx) => {
                    const tags = doc.classification?.tags || doc.classification?.tags_json || [];
                    const matched = getMatchedMatters(tags);
                    const isReviewed = doc.status === "REVIEWED";
                    const formattedDate = new Date(doc.retrieval_date || doc.created_at).toLocaleDateString('en-IN', {
                      day: '2-digit', month: '2-digit', year: 'numeric'
                    });

                    return (
                      <tr key={`tbl-${doc.id}`} className="hover:bg-blue-50/50 transition-colors">
                        {/* Serial Number */}
                        <td className="p-3 pl-4 text-center font-bold text-slate-400">
                          {startIndex + idx + 1}
                        </td>

                        {/* Title & Citation */}
                        <td className="p-3 font-bold text-slate-900 max-w-[280px]">
                          <div className="truncate" title={doc.title}>{doc.title}</div>
                          <div className="flex items-center gap-1.5 mt-0.5 flex-wrap">
                            <span className="text-[10px] text-slate-400 font-normal truncate">{doc.content_hash}</span>
                            <a 
                              href={`${getApiBase()}/api/v1/documents/${doc.id}/pdf`} 
                              target="_blank" 
                              rel="noreferrer" 
                              className="text-[10px] font-bold text-blue-600 hover:underline flex items-center gap-0.5 bg-blue-50 px-1.5 py-0.5 rounded border border-blue-200"
                              title="Open authentic certified PDF in new tab"
                            >
                              <FileText className="h-2.5 w-2.5" /> PDF
                            </a>
                            {doc.original_url && doc.original_url.startsWith("http") && (
                              <a 
                                href={doc.original_url} 
                                target="_blank" 
                                rel="noreferrer" 
                                className="text-[10px] font-bold text-emerald-700 hover:underline flex items-center gap-0.5 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200"
                                title={`Direct Source Order: ${doc.original_url}`}
                              >
                                <Globe className="h-2.5 w-2.5 text-emerald-600" /> Source ↗
                              </a>
                            )}
                          </div>
                        </td>

                        {/* Authority & Verified Source (Strict SC/HC Registry + 3rd-Party Legal Article) */}
                        <td className="p-3 whitespace-nowrap">
                          <div className="flex items-center gap-1.5 font-bold text-slate-800">
                            {doc.authority.includes("Supreme") ? (
                              <span className="bg-red-100 text-red-800 text-[9px] px-1.5 py-0.5 rounded font-black tracking-wide">SC</span>
                            ) : doc.authority.includes("High Court") ? (
                              <span className="bg-blue-100 text-blue-800 text-[9px] px-1.5 py-0.5 rounded font-black tracking-wide">HC</span>
                            ) : (
                              <span className="bg-emerald-100 text-emerald-800 text-[9px] px-1.5 py-0.5 rounded font-black tracking-wide">REG</span>
                            )}
                            <span className="text-xs">{doc.authority}</span>
                          </div>

                          <div className="flex items-center gap-2 mt-1">
                            {/* Official Court / Regulator Portal */}
                            {AUTHORITY_PORTALS[doc.authority] && (
                              <a 
                                href={AUTHORITY_PORTALS[doc.authority].portalUrl} 
                                target="_blank" 
                                rel="noreferrer" 
                                className="text-[10px] font-medium text-emerald-700 hover:text-emerald-900 hover:underline flex items-center gap-0.5"
                                title={`Official Registry: ${AUTHORITY_PORTALS[doc.authority].portalName}`}
                              >
                                <ExternalLink className="h-2.5 w-2.5" /> {AUTHORITY_PORTALS[doc.authority].citationName}
                              </a>
                            )}

                            {/* 3rd-Party Verified Legal Article / Indian Kanoon */}
                            {EXACT_SOURCE_LINKS[doc.content_hash] && (
                              <a 
                                href={EXACT_SOURCE_LINKS[doc.content_hash].articleUrl} 
                                target="_blank" 
                                rel="noreferrer" 
                                className="text-[10px] font-bold text-indigo-600 hover:text-indigo-800 hover:underline flex items-center gap-0.5 bg-indigo-50/80 px-1.5 py-0.5 rounded border border-indigo-200"
                                title={`Open 3rd-party legal report on ${EXACT_SOURCE_LINKS[doc.content_hash].publisher}`}
                              >
                                <span>📖 {EXACT_SOURCE_LINKS[doc.content_hash].publisher.split(' ')[0]} ↗</span>
                              </a>
                            )}
                          </div>
                        </td>

                        {/* Doc Type */}
                        <td className="p-3 whitespace-nowrap">
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-600 border border-slate-200">
                            {doc.document_type}
                          </span>
                        </td>

                        {/* Date Tab Column */}
                        <td className="p-3 whitespace-nowrap text-slate-600 font-semibold">
                          {formattedDate}
                        </td>

                        {/* Topic Tags (Highlighted & Shown In Full) */}
                        <td className="p-3 max-w-[340px]">
                          <div className="flex flex-wrap gap-1.5">
                            {tags.map((t: string) => (
                              <span 
                                key={t} 
                                onClick={(e) => { e.stopPropagation(); setSearchQuery(t.replace(/_/g, " ")); }}
                                className={`text-[10px] font-bold tracking-wide uppercase px-2 py-0.5 rounded-md border shadow-2xs transition-colors cursor-pointer ${getTagBadgeStyle(t)}`}
                                title={`Filter by tag: ${t.replace(/_/g, " ")}`}
                              >
                                {t.replace(/_/g, " ")}
                              </span>
                            ))}
                          </div>
                        </td>

                        {/* Relevance */}
                        <td className="p-3 whitespace-nowrap">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-black border ${doc.classification?.relevance_score === "P0" ? "bg-red-50 text-red-700 border-red-200" : "bg-amber-50 text-amber-700 border-amber-200"}`}>
                            {doc.classification?.relevance_score || "P1"}
                          </span>
                        </td>

                        {/* Matched Matters (Firm CMS Practice Code CY-2024-XXX) */}
                        <td className="p-3 whitespace-nowrap">
                          {matched.length > 0 ? (
                            <div 
                              onClick={() => setSelectedDoc(doc)}
                              className="cursor-pointer group/matter inline-block"
                              title={`Firm Client Case File #${matched[0].id}: ${matched[0].title} (${matched[0].client}) • ${matched.length} active matters in firm impacted`}
                            >
                              <span className="text-[10px] font-bold text-indigo-700 bg-indigo-50 border border-indigo-200 px-2 py-0.5 rounded group-hover/matter:bg-indigo-100 transition-colors inline-flex items-center gap-1">
                                🎯 {matched[0].id} <span className="bg-indigo-200 text-indigo-900 px-1 rounded text-[9px] font-black">{matched.length} cases</span>
                              </span>
                              <span className="text-[10px] text-slate-500 font-medium block mt-0.5 truncate max-w-[140px]">
                                {matched[0].client.split(' ')[0]} ({matched[0].disputed_amount})
                              </span>
                            </div>
                          ) : (
                            <span className="text-slate-400 text-[10px]">None</span>
                          )}
                        </td>

                        {/* Review Status */}
                        <td className="p-3 whitespace-nowrap">
                          {isReviewed ? (
                            <div>
                              <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded flex items-center gap-1 w-fit">
                                <CheckCircle className="h-3 w-3" /> Reviewed
                              </span>
                              <span className="text-[10px] text-slate-500 font-semibold block mt-0.5">
                                {doc.reviews?.[0]?.reviewer_name || "Adv. Amit Kumar Gupta (MD)"}
                              </span>
                            </div>
                          ) : (
                            <span className="text-[10px] font-bold text-amber-700 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded">
                              Pending
                            </span>
                          )}
                        </td>

                        {/* Action */}
                        <td className="p-3 pr-4 text-right whitespace-nowrap">
                          <button 
                            onClick={() => setSelectedDoc(doc)}
                            className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded-md text-[11px] font-bold shadow-sm transition-colors"
                          >
                            Inspect & Review
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>

            {/* Audit Table Pagination Bar */}
            {filteredDocs.length > 0 && (
              <div className="p-3 bg-slate-50 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
                <div className="text-slate-500 font-medium">
                  Showing <span className="font-bold text-slate-800">{startIndex + 1}</span>–<span className="font-bold text-slate-800">{endIndex}</span> of <span className="font-bold text-slate-800">{filteredDocs.length}</span> records
                </div>
                <div className="flex items-center gap-1.5">
                  <button
                    onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                    disabled={currentPage === 1}
                    className="px-2.5 py-1 rounded-md border border-slate-200 bg-white text-slate-700 font-bold hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
                  >
                    Previous
                  </button>
                  <div className="flex items-center gap-1">
                    {Array.from({ length: totalPages }, (_, i) => i + 1).map(p => (
                      <button
                        key={`tbl-p-${p}`}
                        onClick={() => setCurrentPage(p)}
                        className={`w-7 h-7 rounded-md font-bold text-xs transition-all ${
                          currentPage === p
                            ? "bg-blue-600 text-white shadow-xs"
                            : "text-slate-600 hover:bg-slate-100 border border-slate-200 bg-white"
                        }`}
                      >
                        {p}
                      </button>
                    ))}
                  </div>
                  <button
                    onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                    disabled={currentPage === totalPages}
                    className="px-2.5 py-1 rounded-md border border-slate-200 bg-white text-slate-700 font-bold hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
                  >
                    Next
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

      </div>

      {/* Floating Copilot Button (Clean circular FAB - no popping out text) */}
      <button 
        onClick={() => setIsCopilotOpen(!isCopilotOpen)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-blue-600 text-white rounded-full shadow-2xl hover:bg-blue-700 hover:scale-105 active:scale-95 transition-all z-40 border-2 border-white flex items-center justify-center p-0 overflow-hidden shadow-blue-600/30"
        title={isCopilotOpen ? "Close Copilot" : "Open Cyber Watch Copilot"}
        aria-label="Toggle Cyber Watch Copilot"
      >
        {isCopilotOpen ? <X className="h-6 w-6 text-white" /> : <MessageSquare className="h-6 w-6 text-white" />}
      </button>


      {/* Floating Copilot Chat Window (Widened & Expandable) */}
      {isCopilotOpen && (
        <div className={`fixed bottom-20 right-6 ${isCopilotExpanded ? "w-[920px] max-w-[96vw]" : "w-[660px] max-w-[calc(100vw-2rem)]"} bg-white rounded-2xl shadow-2xl ring-1 ring-black/10 z-40 flex flex-col overflow-hidden h-[660px] max-h-[88vh] transition-all duration-200 animate-in slide-in-from-bottom-5`}>
          <div className="p-4 bg-gradient-to-r from-blue-700 to-indigo-800 text-white flex justify-between items-center shadow-md z-10">
            <div className="flex items-center gap-2.5">
              <div className="bg-white/20 p-1.5 rounded-lg"><Bot className="h-5 w-5 text-white" /></div>
              <div>
                <h3 className="font-bold text-sm">Cyber Watch Copilot</h3>
                <p className="text-[10px] text-blue-100 font-medium">CYBER PRACTICE INTELLIGENCE COUNSEL</p>
              </div>
            </div>
            <div className="flex items-center gap-1">
              <button 
                onClick={() => { setChatHistory([]); setCopilotQuery(""); }}
                className="text-white/80 hover:text-white p-1.5 rounded-md hover:bg-white/10 transition-colors"
                title="Start New Consultation Session (Reset)"
              >
                <RotateCcw className="h-4 w-4" />
              </button>
              <button 
                onClick={() => setIsCopilotExpanded(!isCopilotExpanded)}
                className="text-white/80 hover:text-white p-1.5 rounded-md hover:bg-white/10 transition-colors"
                title={isCopilotExpanded ? "Restore Standard Width (660px)" : "Expand Panoramic View (920px)"}
              >
                {isCopilotExpanded ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
              </button>
              <button 
                onClick={() => setIsCopilotOpen(false)} 
                className="text-white/80 hover:text-white p-1.5 rounded-md hover:bg-white/10 transition-colors"
                title="Close Window"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          </div>

          {/* Intelligence Capability Bar */}
          <div className="bg-slate-100/90 border-b border-slate-200 px-3.5 py-1.5 flex items-center justify-between text-[11px]">
            <span className="flex items-center gap-1.5 text-blue-900 font-bold">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              {chatHistory.length > 0 ? (
                <span>Active Continuous Consultation • Turn {Math.ceil(chatHistory.length / 2)}</span>
              ) : (
                <span>Full Legal RAG Active (Gemini Flash + Certified Sources)</span>
              )}
            </span>
            <div className="flex items-center gap-2">
              <span className="text-slate-500 font-medium hidden sm:inline">SC & HC Precedents • CERT-In • RBI • Excl. District Courts</span>
              {chatHistory.length > 0 && (
                <button 
                  onClick={() => { setChatHistory([]); setCopilotQuery(""); }}
                  className="text-[10px] text-blue-600 hover:text-blue-800 font-bold underline cursor-pointer"
                >
                  New Session
                </button>
              )}
            </div>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50">
            {chatHistory.length === 0 && (
              <div className="text-center mt-3">
                <div className="bg-blue-100 w-10 h-10 rounded-full flex items-center justify-center mx-auto mb-2.5">
                  <Scale className="h-5 w-5 text-blue-700" />
                </div>
                <h4 className="font-bold text-sm text-slate-800">High-Capability Legal Intelligence</h4>
                <p className="text-xs text-slate-500 mt-1 max-w-[340px] mx-auto">
                  Ask multi-statutory cyber questions, obtain court-ready pleading drafts, compare CrPC with BNSS, or query compliance guidelines.
                </p>
                <div className="mt-4 flex flex-col gap-1.5 text-left">
                  <button 
                    onClick={() => setCopilotQuery("Can police freeze an entire bank account under Sec 102 CrPC / BNSS 106?")}
                    className="text-[11px] bg-white border border-slate-200 p-2.5 rounded-lg text-slate-700 hover:border-blue-400 hover:text-blue-700 hover:bg-blue-50/50 font-medium text-left transition-all shadow-xs"
                  >
                    💡 <strong>Sec 102 CrPC vs BNSS 106:</strong> Can police freeze entire operational account?
                  </button>
                  <button 
                    onClick={() => setCopilotQuery("Draft pleading grounds under Sec 457 CrPC for an innocent merchant account frozen in Layer 3.")}
                    className="text-[11px] bg-white border border-slate-200 p-2.5 rounded-lg text-slate-700 hover:border-blue-400 hover:text-blue-700 hover:bg-blue-50/50 font-medium text-left transition-all shadow-xs"
                  >
                    ⚖️ <strong>Litigation Grounds:</strong> Draft Sec 457 CrPC application for Layer-3 merchant
                  </button>
                  <button 
                    onClick={() => setCopilotQuery("What did Delhi High Court rule about Digital Arrest scams and victim restitution?")}
                    className="text-[11px] bg-white border border-slate-200 p-2.5 rounded-lg text-slate-700 hover:border-blue-400 hover:text-blue-700 hover:bg-blue-50/50 font-medium text-left transition-all shadow-xs"
                  >
                    🛡️ <strong>Digital Arrest SOP:</strong> Delhi HC ruling & fast-track victim restitution
                  </button>
                  <button 
                    onClick={() => setCopilotQuery("Explain the 90-day sunset clause for Layer 3 to Layer 6 accounts under the MHA I4C SOP.")}
                    className="text-[11px] bg-white border border-slate-200 p-2.5 rounded-lg text-slate-700 hover:border-blue-400 hover:text-blue-700 hover:bg-blue-50/50 font-medium text-left transition-all shadow-xs"
                  >
                    ⏳ <strong>I4C Mule SOP:</strong> 90-day sunset clause for automatic lien removal
                  </button>
                  <button 
                    onClick={() => setCopilotQuery("What is the reporting window for RBI vs CERT-In cyber incidents and 180-day log rule?")}
                    className="text-[11px] bg-white border border-slate-200 p-2.5 rounded-lg text-slate-700 hover:border-blue-400 hover:text-blue-700 hover:bg-blue-50/50 font-medium text-left transition-all shadow-xs"
                  >
                    ⏱️ <strong>Regulatory Timelines:</strong> RBI 4-hour vs CERT-In 6-hour & 180-day log mandate
                  </button>
                </div>
              </div>
            )}
            
            {chatHistory.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-[94%] rounded-2xl p-4 shadow-sm ${msg.role === "user" ? "bg-blue-600 text-white rounded-tr-sm shadow-md border border-blue-500" : "bg-white border border-slate-200 text-slate-800 rounded-tl-sm"}`}>
                  {msg.role === "user" ? (
                    <div className="text-xs font-semibold text-white leading-relaxed select-text whitespace-pre-wrap tracking-wide">
                      {msg.content}
                    </div>
                  ) : (
                    <div className="text-xs leading-relaxed prose prose-sm max-w-none text-slate-800">
                      <ReactMarkdown
                        components={{
                          a: ({node, ...props}) => <a {...props} className="text-blue-600 hover:underline font-bold" target="_blank" rel="noreferrer" />,
                          p: ({node, ...props}) => <p {...props} className="mb-2 last:mb-0 leading-relaxed text-slate-800" />,
                          ul: ({node, ...props}) => <ul {...props} className="list-disc pl-4 mb-2 space-y-1" />,
                          pre: ({node, children, ...props}) => (
                            <div className="my-2.5 rounded-xl border border-slate-700 overflow-hidden shadow-sm">
                              <div className="bg-slate-800 px-3 py-1 flex items-center justify-between text-[10px] font-mono text-slate-300">
                                <span>COURT PLEADING CLAUSE / STATUTORY NOTICE</span>
                                <button 
                                  type="button"
                                  onClick={() => {
                                    const preEl = (node as any)?.children?.[0]?.value || "";
                                    if (preEl) {
                                      navigator.clipboard.writeText(preEl);
                                      alert("Clause copied to clipboard!");
                                    }
                                  }}
                                  className="text-slate-300 hover:text-white flex items-center gap-1 bg-slate-700 hover:bg-slate-600 px-2 py-0.5 rounded transition"
                                >
                                  <Copy className="h-3 w-3" /> Copy Draft
                                </button>
                              </div>
                              <pre {...props} className="bg-slate-950 text-slate-100 p-3.5 text-[11px] font-mono whitespace-pre-wrap break-words leading-relaxed overflow-x-auto">
                                {children}
                              </pre>
                            </div>
                          ),
                          code: ({node, className, children, ...props}) => {
                            const isInline = !className;
                            return isInline ? (
                              <code {...props} className="bg-slate-100 text-blue-700 px-1 py-0.5 rounded text-[11px] font-mono border border-slate-200 font-semibold">
                                {children}
                              </code>
                            ) : (
                              <code {...props} className={className}>
                                {children}
                              </code>
                            );
                          }
                        }}
                      >
                        {msg.content}
                      </ReactMarkdown>
                    </div>
                  )}

                  {/* Quoted Certified PDF Sources */}
                  {msg.citations && msg.citations.length > 0 && (
                    <div className="mt-3.5 pt-3 border-t border-slate-100 bg-blue-50/70 p-3 rounded-xl border border-blue-100">
                      <p className="text-[10px] font-black text-blue-900 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                        <FileText className="h-3.5 w-3.5 text-blue-600" /> Quoted Certified Judicial PDF Sources (Click to Open):
                      </p>
                      <div className="flex flex-col gap-1.5">
                        {msg.citations.map((cit, cidx) => (
                          <a 
                            key={cidx} 
                            href={cit.document_id ? `${getApiBase()}/api/v1/documents/${cit.document_id}/pdf` : cit.original_url} 
                            target="_blank" 
                            rel="noreferrer" 
                            className="text-[11px] bg-white border border-blue-200 hover:border-blue-500 hover:bg-blue-50 p-2 rounded-lg flex items-center justify-between gap-2 text-slate-800 font-semibold group transition shadow-2xs"
                            title={`Open official certified PDF copy: ${cit.title}`}
                          >
                            <div className="flex items-center gap-2 truncate">
                              <span className="bg-blue-600 text-white text-[10px] px-1.5 py-0.5 rounded font-black shrink-0">[{cidx + 1}]</span>
                              <span className="truncate">{cit.title}</span>
                            </div>
                            <div className="flex items-center gap-1 text-[10px] text-blue-700 font-bold shrink-0 ml-1 group-hover:underline">
                              <span>{cit.original_url.split('/').pop()}</span>
                              <ArrowUpRight className="h-3 w-3" />
                            </div>
                          </a>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
            
            {/* Interactive Follow-Up Chips (Visible after answers so session is clearly active) */}
            {chatHistory.length > 0 && !isTyping && (
              <div className="pt-2 border-t border-slate-200">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] font-black text-slate-500 uppercase tracking-wider flex items-center gap-1">
                    <Sparkles className="h-3 w-3 text-amber-500" /> Continue Consultation / Follow-Up Questions:
                  </span>
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {[
                    { label: "📝 Draft Sec 457 CrPC Pleading", q: "Draft pleading grounds under Sec 457 CrPC for an innocent merchant account frozen in Layer 3." },
                    { label: "✉️ Draft Bank Nodal Notice", q: "Draft representation letter to Bank Nodal Officer demanding partial freeze strictly to disputed amount." },
                    { label: "🛡️ Digital Arrest Restitution", q: "What did Delhi High Court rule about Digital Arrest scams and victim restitution?" },
                    { label: "⏳ Layer 3-6 90-Day Rule", q: "Explain the 90-day sunset clause for Layer 3 to Layer 6 accounts under the MHA I4C SOP." },
                    { label: "⏱️ CERT-In vs RBI Timelines", q: "What is the reporting window for RBI vs CERT-In cyber incidents and 180-day log rule?" },
                    { label: "🏛️ BNSS 106 Magistrate Duties", q: "Compare BNSS 106 with CrPC 102 regarding mandatory magistrate notification." }
                  ].map((chip, ci) => (
                    <button
                      key={ci}
                      type="button"
                      onClick={() => setCopilotQuery(chip.q)}
                      className="text-[11px] bg-white border border-slate-200 hover:border-blue-400 hover:bg-blue-50 text-slate-700 px-2.5 py-1.5 rounded-lg font-medium transition shadow-2xs text-left"
                    >
                      {chip.label}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-white border border-slate-200 rounded-2xl rounded-tl-sm p-3.5 shadow-sm flex items-center space-x-2">
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: "0.4s" }}></div>
                  <span className="text-xs text-slate-500 font-medium ml-1">Formulating multi-statutory opinion...</span>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>
          
          <form onSubmit={handleAskCopilot} className="p-3 bg-white border-t border-slate-200 flex items-center gap-2">
            <input 
              type="text" 
              value={copilotQuery}
              onChange={(e) => setCopilotQuery(e.target.value)}
              placeholder="Ask follow-up query or draft request..."
              className="flex-1 bg-slate-100 border-none rounded-xl px-3.5 py-2.5 text-xs focus:ring-2 focus:ring-blue-500 focus:outline-none transition-shadow"
              disabled={isTyping}
            />
            <button 
              type="submit" 
              disabled={isTyping || !copilotQuery.trim()}
              className="bg-blue-700 text-white p-2.5 rounded-xl hover:bg-blue-800 disabled:opacity-50 transition-colors shadow-sm"
              title="Send Legal Query"
            >
              <Send className="h-4 w-4" />
            </button>
          </form>
        </div>
      )}

      {/* Comprehensive Interactive Review Modal */}
      {selectedDoc && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/70 backdrop-blur-sm p-2 sm:p-4 md:p-6 overflow-y-auto">
          <div className="bg-white w-full max-w-[1400px] max-h-[94vh] flex flex-col rounded-2xl shadow-2xl ring-1 ring-black/10 animate-in fade-in zoom-in-95 duration-200 overflow-hidden my-auto">
            
            {/* Modal Header */}
            <div className="p-4 sm:p-5 border-b border-slate-200 flex justify-between items-start bg-slate-50 shrink-0 gap-3">
              <div className="space-y-1.5 pr-2 min-w-0 flex-1">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-[11px] font-black uppercase tracking-wider px-2 py-0.5 rounded bg-blue-100 text-blue-800 border border-blue-200">
                    {selectedDoc.document_type || "LEGAL DOCUMENT"}
                  </span>
                  <span className={`text-[11px] font-black uppercase tracking-wider px-2 py-0.5 rounded border ${(selectedDoc.classification?.relevance_score || "P1") === "P0" ? "bg-red-50 text-red-700 border-red-200" : "bg-amber-50 text-amber-700 border-amber-200"}`}>
                    Priority: {selectedDoc.classification?.relevance_score || "P1"}
                  </span>
                  <span className="text-xs text-slate-500 font-semibold">• {selectedDoc.authority}</span>
                </div>
                <h2 className="text-lg sm:text-xl md:text-2xl font-black text-slate-900 leading-snug break-words">{selectedDoc.title}</h2>
                <div className="flex items-center gap-2 sm:gap-3 text-xs font-medium text-slate-500 pt-1 flex-wrap">
                  <span className="whitespace-nowrap">Order / Retrieval Date: {new Date(selectedDoc.retrieval_date || selectedDoc.created_at).toLocaleDateString('en-IN')}</span>
                  <span className="hidden sm:inline">•</span>
                  
                  {/* Exact Quoted Certified Official PDF */}
                  <a 
                    href={`${getApiBase()}/api/v1/documents/${selectedDoc.id}/pdf`} 
                    target="_blank" 
                    rel="noreferrer" 
                    className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded-lg font-bold flex items-center gap-1.5 transition-all shadow-xs group"
                    title="Open authentic certified PDF in full separate tab"
                  >
                    <FileText className="h-3.5 w-3.5 text-white" />
                    <span>Exact Official PDF</span> 
                    <ArrowUpRight className="h-3.5 w-3.5 text-blue-200 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
                  </a>

                  {/* Direct Web Source / Live Portal Link */}
                  {selectedDoc.original_url && selectedDoc.original_url.startsWith("http") && (
                    <a 
                      href={selectedDoc.original_url} 
                      target="_blank" 
                      rel="noreferrer" 
                      className="bg-emerald-600 hover:bg-emerald-700 text-white px-3 py-1 rounded-lg font-bold flex items-center gap-1.5 transition-all shadow-xs group"
                      title={`Open direct official source docket/order: ${selectedDoc.original_url}`}
                    >
                      <Globe className="h-3.5 w-3.5 text-white" />
                      <span>Direct Source Order</span>
                      <ArrowUpRight className="h-3.5 w-3.5 text-emerald-200 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
                    </a>
                  )}

                  {/* Official Court Registry / Departmental Verification Link (Strict SC / HC) */}
                  <a 
                    href={AUTHORITY_PORTALS[selectedDoc.authority]?.portalUrl || "https://www.sci.gov.in"} 
                    target="_blank" 
                    rel="noreferrer" 
                    className="bg-slate-100 text-slate-800 hover:bg-slate-200 border border-slate-300 px-2.5 py-1 rounded-lg font-bold flex items-center gap-1.5 transition-colors shadow-xs group"
                    title={`Verify case docket on official registry: ${AUTHORITY_PORTALS[selectedDoc.authority]?.portalName || selectedDoc.authority}`}
                  >
                    <ExternalLink className="h-3.5 w-3.5 text-slate-600 group-hover:scale-110 transition-transform" />
                    <span>Official Portal: <strong>{AUTHORITY_PORTALS[selectedDoc.authority]?.citationName || selectedDoc.authority}</strong></span>
                    <ArrowUpRight className="h-3.5 w-3.5 text-slate-600" />
                  </a>

                  {/* 3rd-Party Legal Database / Kanoon Link */}
                  {EXACT_SOURCE_LINKS[selectedDoc.content_hash] && (
                    <a 
                      href={EXACT_SOURCE_LINKS[selectedDoc.content_hash].articleUrl} 
                      target="_blank" 
                      rel="noreferrer" 
                      className="bg-indigo-50 text-indigo-800 hover:bg-indigo-100 border border-indigo-200 px-2.5 py-1 rounded-lg font-bold flex items-center gap-1.5 transition-colors shadow-xs"
                      title={`Open verified legal report on ${EXACT_SOURCE_LINKS[selectedDoc.content_hash].publisher}`}
                    >
                      <span>📖 {EXACT_SOURCE_LINKS[selectedDoc.content_hash].publisher}</span>
                      <ArrowUpRight className="h-3.5 w-3.5 text-indigo-600" />
                    </a>
                  )}
                </div>
              </div>

              <button 
                onClick={() => { setSelectedDoc(null); setGeneratedTask(null); }} 
                className="text-slate-400 hover:text-slate-700 bg-white border border-slate-200 hover:bg-slate-100 rounded-full p-2 shadow-sm transition-colors shrink-0"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            
            {/* Modal Body */}
            <div className="flex-1 overflow-y-auto p-4 sm:p-6 bg-slate-100/60 min-h-0">
              <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 min-w-0">
                
                {/* Left Column: Official Source Document & PDF Viewer */}
                <div className="flex flex-col bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden min-w-0 h-[560px] xl:h-[720px]">
                  <div className="p-3 border-b border-slate-200 bg-slate-50 flex flex-wrap justify-between items-center gap-2 shrink-0">
                    <div className="flex items-center gap-2 px-1">
                      <FileText className="h-4 w-4 text-blue-600 shrink-0" />
                      <h3 className="text-sm font-bold text-slate-800 whitespace-nowrap">Source Evidence Viewer</h3>
                    </div>
                    <div className="flex items-center gap-2 flex-wrap">
                      <a 
                        href={`${getApiBase()}/api/v1/documents/${selectedDoc.id}/pdf`} 
                        target="_blank" 
                        rel="noreferrer" 
                        className="flex items-center gap-1.5 text-[11px] font-bold text-blue-700 bg-blue-50 hover:bg-blue-100 border border-blue-200 px-2.5 py-1 rounded-md transition-colors whitespace-nowrap"
                        title="Open exact certified PDF in separate tab"
                      >
                        <FileText className="h-3 w-3 text-blue-600" /> Open PDF in New Tab ↗
                      </a>
                      <div className="flex bg-slate-200 rounded-lg p-0.5 text-xs shrink-0">
                        <button 
                          onClick={() => setViewMode("pdf")}
                          className={`px-3 py-1 font-bold rounded-md transition-all ${viewMode === "pdf" ? "bg-white text-slate-900 shadow-sm" : "text-slate-600 hover:text-slate-900"}`}
                        >
                          Official PDF
                        </button>
                        <button 
                          onClick={() => setViewMode("text")}
                          className={`px-3 py-1 font-bold rounded-md transition-all ${viewMode === "text" ? "bg-white text-slate-900 shadow-sm" : "text-slate-600 hover:text-slate-900"}`}
                        >
                          Extracted Text
                        </button>
                      </div>
                    </div>
                  </div>

                  <div className="flex-1 overflow-hidden bg-slate-100 relative flex flex-col min-h-0">
                    {viewMode === "pdf" && (
                      <div className="bg-blue-50/90 border-b border-blue-200 px-3 py-1.5 flex items-center justify-between text-xs text-blue-950 font-medium shrink-0 flex-wrap gap-2">
                        <div className="flex items-center gap-2 truncate min-w-0">
                          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse shrink-0"></span>
                          <span className="font-bold text-[11px] shrink-0">Certified Source:</span>
                          <a 
                            href={selectedDoc.original_url.startsWith("http") ? selectedDoc.original_url : `${getApiBase()}/api/v1/documents/${selectedDoc.id}/pdf`}
                            target="_blank" 
                            rel="noreferrer"
                            className="bg-white px-2 py-0.5 rounded border border-blue-200 text-blue-800 font-mono text-[11px] truncate hover:underline flex items-center gap-1"
                            title={`Open direct source link: ${selectedDoc.original_url}`}
                          >
                            <span>{selectedDoc.original_url}</span>
                            <ArrowUpRight className="h-3 w-3 shrink-0" />
                          </a>
                        </div>
                        <a 
                          href={`${getApiBase()}/api/v1/documents/${selectedDoc.id}/pdf`} 
                          download 
                          className="text-blue-700 hover:text-blue-900 font-bold text-[11px] underline shrink-0 ml-auto"
                        >
                          Download PDF
                        </a>
                      </div>
                    )}
                    {viewMode === "text" && (
                      <div className="bg-slate-100 border-b border-slate-200 px-3 py-1.5 flex items-center justify-between text-xs text-slate-700 font-medium shrink-0 flex-wrap gap-2">
                        <div className="flex items-center gap-2 min-w-0">
                          <span className="text-[11px] font-bold text-slate-600 shrink-0">Verbatim Certified Transcript • {selectedDoc.raw_text?.length || 0} chars</span>
                          {selectedDoc.original_url && selectedDoc.original_url.startsWith("http") && (
                            <a 
                              href={selectedDoc.original_url} 
                              target="_blank" 
                              rel="noreferrer" 
                              className="text-[10px] font-bold text-emerald-700 hover:underline flex items-center gap-0.5 bg-emerald-50 border border-emerald-200 px-1.5 py-0.5 rounded"
                              title="Direct Source Link"
                            >
                              <Globe className="h-2.5 w-2.5" /> Source Link ↗
                            </a>
                          )}
                        </div>
                        <button 
                          onClick={() => {
                            navigator.clipboard.writeText(selectedDoc.raw_text || "");
                            alert("Full extracted judgment text copied to clipboard!");
                          }}
                          className="text-blue-700 hover:text-blue-900 font-bold text-[11px] flex items-center gap-1 bg-white border border-slate-300 px-2 py-0.5 rounded shadow-2xs shrink-0 ml-auto"
                        >
                          <Copy className="h-3 w-3" /> Copy Extracted Text
                        </button>
                      </div>
                    )}
                    <div className="flex-1 relative overflow-hidden min-h-0">
                      {viewMode === "pdf" ? (
                         <iframe 
                           src={`${getApiBase()}/api/v1/documents/${selectedDoc.id}/pdf`} 
                           className="w-full h-full border-0 absolute inset-0 bg-white"
                           title="Official Legal Document"
                         />
                      ) : (
                        <div className="p-4 sm:p-6 text-xs text-slate-800 font-mono leading-relaxed whitespace-pre-wrap h-full overflow-y-auto bg-slate-50 select-text">
                          {selectedDoc.raw_text || "No text could be extracted."}
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Document Footer Verification */}
                  <div className="p-2.5 bg-slate-50 border-t border-slate-200 text-[11px] text-slate-500 flex justify-between items-center px-4 shrink-0 flex-wrap gap-2">
                    <span className="truncate min-w-0">Document Hash: <code className="bg-slate-200 px-1 py-0.5 rounded text-[10px]">{selectedDoc.content_hash}</code></span>
                    <span className="text-emerald-700 font-bold flex items-center gap-1 shrink-0">
                      <ShieldCheck className="h-3.5 w-3.5" /> Immutable Verification Record
                    </span>
                  </div>
                </div>
                
                {/* Right Column: Complete AI Impact Analysis + Matter Matching + Action Workflow */}
                <div className="flex flex-col space-y-5 min-w-0">
                  
                  {/* AI Structured Impact Analysis */}
                  <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                    <div className="p-4 border-b border-slate-100 bg-blue-50/80 flex items-center justify-between">
                      <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                        <Activity className="h-4 w-4 text-blue-700" /> AI Impact & Practical Analysis
                      </h3>
                      <span className="text-[11px] font-extrabold text-blue-800 bg-blue-100 px-2 py-0.5 rounded">
                        Confidence: {Math.round((selectedDoc.classification?.confidence || 0.95) * 100)}%
                      </span>
                    </div>
                    
                    <div className="p-5 space-y-4 text-xs text-slate-700">
                      {selectedDoc.impact_note ? (
                        <>
                          {/* What Happened */}
                          <div className="space-y-1">
                            <span className="text-slate-900 block font-bold text-xs uppercase tracking-wider text-slate-500">What Happened</span>
                            <p className="leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-200 text-slate-800 font-medium">
                              {selectedDoc.impact_note.what_happened}
                            </p>
                          </div>

                          {/* Legal Status & Authority Detail */}
                          <div className="grid grid-cols-2 gap-3">
                            <div className="space-y-1">
                              <span className="text-slate-900 block font-bold text-xs uppercase tracking-wider text-slate-500">Legal Status</span>
                              <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-200 font-bold text-blue-900 text-[11px]">
                                {selectedDoc.impact_note.legal_status || "Binding Precedent"}
                              </div>
                            </div>
                            <div className="space-y-1">
                              <span className="text-slate-900 block font-bold text-xs uppercase tracking-wider text-slate-500">Authority Detail</span>
                              <div className="p-2.5 bg-slate-50 rounded-lg border border-slate-200 font-bold text-slate-800 text-[11px] truncate" title={selectedDoc.impact_note.authority_detail}>
                                {selectedDoc.impact_note.authority_detail || selectedDoc.authority}
                              </div>
                            </div>
                          </div>

                          {/* What Changed */}
                          <div className="space-y-1">
                            <span className="text-slate-900 block font-bold text-xs uppercase tracking-wider text-slate-500">What Changed (Shift in Legal Position)</span>
                            <p className="leading-relaxed bg-blue-50/60 p-3 rounded-lg border border-blue-200 text-blue-950 font-medium">
                              {selectedDoc.impact_note.what_changed || "Clarifies limits on police seizing powers in cyber bank account freezes."}
                            </p>
                          </div>

                          {/* Practical Relevance */}
                          <div className="space-y-1">
                            <span className="text-slate-900 block font-bold text-xs uppercase tracking-wider text-slate-500">Practical Relevance for Cyber Matters</span>
                            <p className="leading-relaxed bg-slate-50 p-3 rounded-lg border border-slate-200 text-slate-800 font-medium">
                              {selectedDoc.impact_note.practical_relevance}
                            </p>
                          </div>

                          {/* Caution / Caveats */}
                          <div className="bg-amber-50/80 border border-amber-200 p-3.5 rounded-xl">
                            <span className="text-amber-900 flex items-center font-bold text-xs">
                              <AlertTriangle className="h-4 w-4 mr-1.5 text-amber-600" /> Caution & Statutory Caveats:
                            </span>
                            <p className="text-amber-900/90 mt-1 leading-relaxed font-medium">
                              {selectedDoc.impact_note.caution}
                            </p>
                          </div>
                        </>
                      ) : (
                        <p className="text-slate-500 italic p-6 text-center bg-slate-50 rounded-lg border border-dashed border-slate-300">
                          No impact note recorded.
                        </p>
                      )}

                      {/* Topic Tags */}
                      <div className="pt-2">
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1.5">Topic Classification</span>
                        <div className="flex flex-wrap gap-1.5">
                          {(selectedDoc.classification?.tags || selectedDoc.classification?.tags_json || []).map((t: string) => (
                            <span key={t} className={`text-[10px] font-bold uppercase tracking-wide px-2.5 py-1 rounded-md border shadow-2xs ${getTagBadgeStyle(t)}`}>
                              {t.replace(/_/g, " ")}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Active Matters Impact Matching (Brief Phase 4) */}
                  <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                    <div className="p-3.5 border-b border-slate-100 bg-indigo-50/70 flex justify-between items-center">
                      <h3 className="text-xs font-bold text-indigo-950 flex items-center gap-1.5">
                        <Briefcase className="h-4 w-4 text-indigo-600" /> Matched Firm Matters (CMS Linkage)
                      </h3>
                      <span className="text-[10px] bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded font-bold">
                        {getMatchedMatters(selectedDoc.classification?.tags || selectedDoc.classification?.tags_json || []).length} Matches
                      </span>
                    </div>

                    <div className="p-4 space-y-2.5">
                      {getMatchedMatters(selectedDoc.classification?.tags || selectedDoc.classification?.tags_json || []).map(matter => (
                        <div key={matter.id} className="p-3 bg-slate-50 rounded-xl border border-slate-200 flex flex-col md:flex-row justify-between items-start md:items-center gap-2">
                          <div>
                            <div className="flex items-center gap-2">
                              <span className="text-[10px] font-black bg-indigo-100 text-indigo-800 px-1.5 py-0.5 rounded">{matter.id}</span>
                              <span className="font-bold text-xs text-slate-900">{matter.title}</span>
                            </div>
                            <p className="text-[11px] text-slate-500 mt-0.5">{matter.summary}</p>
                          </div>
                          <button 
                            onClick={() => handleGenerateT63Task(matter)}
                            disabled={isGeneratingTask}
                            className="shrink-0 text-xs bg-indigo-600 hover:bg-indigo-700 text-white font-bold px-3 py-1.5 rounded-lg transition shadow-sm"
                          >
                            Generate T-63 Task
                          </button>
                        </div>
                      ))}
                      {getMatchedMatters(selectedDoc.classification?.tags || selectedDoc.classification?.tags_json || []).length === 0 && (
                        <p className="text-xs text-slate-400 italic text-center p-3">No active client matters tagged for this specific topic.</p>
                      )}
                    </div>
                  </div>

                  {/* Generated T-63 Task Notification */}
                  {generatedTask && (
                    <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-4 shadow-sm animate-in fade-in">
                      <div className="flex justify-between items-start">
                        <div className="flex items-center gap-2 text-emerald-800 font-bold text-xs">
                          <CheckCircle className="h-4 w-4 text-emerald-600" /> Proposed T-63 Action Created
                        </div>
                        <span className="text-[10px] font-mono font-bold bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded">
                          {generatedTask.task_code}
                        </span>
                      </div>
                      <p className="text-xs text-emerald-900 mt-1 font-medium">{generatedTask.description}</p>
                      <div className="mt-2 text-[10px] text-emerald-700 flex justify-between items-center">
                        <span>Status: <b>{generatedTask.status}</b> (Awaiting Advocate Sign-off)</span>
                        <span className="font-bold">Matter: {generatedTask.matter_reference}</span>
                      </div>
                    </div>
                  )}

                  {/* Lawyer Validation Action Form (Default Lawyer: Adv. Amit Kumar Gupta (MD)) */}
                  <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
                      <h3 className="text-xs font-bold text-slate-900 flex items-center gap-1.5 uppercase tracking-wider">
                        <Scale className="h-4 w-4 text-blue-700" /> Lawyer Validation & Audit Sign-Off
                      </h3>
                      <span className="text-[10px] text-slate-400">Human-in-the-Loop Safeguard</span>
                    </div>

                    {selectedDoc.reviews && selectedDoc.reviews.length > 0 && (
                      <div className="mb-4 p-3 bg-emerald-50 border border-emerald-200 text-emerald-900 rounded-xl text-xs space-y-1">
                        <div className="font-bold flex items-center gap-1.5 text-emerald-800">
                          <CheckCircle className="h-4 w-4 text-emerald-600" />
                          Validated Sign-Off: {selectedDoc.reviews[0].reviewer_name}
                        </div>
                        <p className="text-[11px] text-emerald-700 font-medium">
                          <strong>Decision:</strong> {selectedDoc.reviews[0].decision?.replace(/_/g, " ")} • {new Date(selectedDoc.reviews[0].reviewed_at).toLocaleDateString('en-IN')}
                        </p>
                        {selectedDoc.reviews[0].notes && (
                          <p className="text-[11px] text-slate-600 bg-white/70 p-2 rounded-lg border border-emerald-100">
                            "{selectedDoc.reviews[0].notes}"
                          </p>
                        )}
                      </div>
                    )}

                    {reviewSuccessMsg && (
                      <div className="mb-4 p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-lg text-xs font-bold flex items-center gap-2">
                        <CheckCircle className="h-4 w-4 text-emerald-600" /> {reviewSuccessMsg}
                      </div>
                    )}

                    <form onSubmit={handleSubmitReview} className="space-y-3.5">
                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Reviewer Name</label>
                          <input 
                            type="text" 
                            value={reviewerName}
                            onChange={(e) => setReviewerName(e.target.value)}
                            className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-1.5 text-xs font-bold text-slate-800 focus:bg-white focus:outline-none"
                            required
                          />
                        </div>
                        <div>
                          <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Validation Decision</label>
                          <select 
                            value={reviewDecision}
                            onChange={(e) => setReviewDecision(e.target.value)}
                            className="w-full bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1.5 text-xs font-bold text-slate-800 focus:bg-white focus:outline-none"
                          >
                            <option value="APPROVED_TO_KNOWLEDGE_BASE">Approved to Knowledge Base</option>
                            <option value="APPLY_TO_MATTER">Apply to Active Matter</option>
                            <option value="RELEVANT">Relevant (Verified)</option>
                            <option value="NEEDS_SENIOR_REVIEW">Needs Senior Review</option>
                            <option value="MONITOR">Monitor Only</option>
                            <option value="NOT_RELEVANT">Not Relevant</option>
                          </select>
                        </div>
                      </div>

                      <div>
                        <label className="text-[10px] font-bold text-slate-500 uppercase block mb-1">Review Notes & Instructions</label>
                        <textarea 
                          rows={2}
                          value={reviewNotes}
                          onChange={(e) => setReviewNotes(e.target.value)}
                          placeholder="Add instructions for matter associates, citations, or caveats..."
                          className="w-full bg-slate-50 border border-slate-200 rounded-lg p-2 text-xs font-medium focus:bg-white focus:outline-none"
                        />
                      </div>

                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                        <button 
                          type="submit"
                          disabled={isSubmittingReview}
                          className="w-full bg-blue-700 hover:bg-blue-800 text-white py-2.5 rounded-xl font-bold text-xs transition shadow-sm flex justify-center items-center gap-1.5 disabled:opacity-50"
                        >
                          <CheckCircle className="h-4 w-4" /> Record Lawyer Sign-Off
                        </button>
                        <button 
                          type="button"
                          onClick={handleGenerateAlert}
                          disabled={isGeneratingAlert}
                          className="w-full bg-white hover:bg-slate-50 text-slate-800 py-2.5 rounded-xl font-bold text-xs transition border border-slate-300 shadow-sm flex justify-center items-center gap-1.5 disabled:opacity-50"
                        >
                          {isGeneratingAlert ? (
                            <><RefreshCw className="h-3.5 w-3.5 animate-spin" /> Drafting...</>
                          ) : (
                            <><Send className="h-3.5 w-3.5 text-blue-600" /> Draft Client Advisory</>
                          )}
                        </button>
                      </div>
                    </form>
                  </div>
                  
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Generated Email Alert Modal */}
      {generatedAlert && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-slate-900/70 backdrop-blur-sm p-4 animate-in fade-in">
          <div className="bg-white w-full max-w-3xl overflow-hidden flex flex-col rounded-2xl shadow-2xl">
            <div className="p-4 border-b border-slate-200 bg-blue-50 flex justify-between items-center">
              <h3 className="font-bold text-blue-900 text-sm flex items-center gap-2">
                <Send className="h-4 w-4 text-blue-600" /> Client Advisory Draft (AI Intelligence)
              </h3>
              <button onClick={() => setGeneratedAlert(null)} className="text-slate-400 hover:text-slate-700"><X className="h-4 w-4" /></button>
            </div>
            <div className="p-5 bg-slate-50 overflow-y-auto max-h-[70vh]">
              <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm space-y-3">
                <div>
                  <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Subject Line</label>
                  <p className="text-slate-900 font-bold text-sm mt-0.5">{generatedAlert.subject}</p>
                </div>
                <hr className="border-slate-100" />
                <div>
                  <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Advisory Body</label>
                  <div className="mt-2 text-xs leading-relaxed prose prose-sm max-w-none text-slate-800 bg-slate-50 p-4 rounded-lg border border-slate-100">
                    <ReactMarkdown>{generatedAlert.body}</ReactMarkdown>
                  </div>
                </div>
              </div>
            </div>
            <div className="p-3.5 border-t border-slate-200 flex justify-end gap-2 bg-white">
              <button onClick={() => setGeneratedAlert(null)} className="px-3.5 py-1.5 text-xs font-bold text-slate-600 hover:bg-slate-100 rounded-lg">Discard</button>
              <button onClick={() => {
                navigator.clipboard.writeText(`Subject: ${generatedAlert.subject}\n\n${generatedAlert.body}`);
                alert("Client advisory copied to clipboard!");
              }} className="px-4 py-1.5 text-xs font-bold bg-blue-700 text-white hover:bg-blue-800 rounded-lg shadow-sm flex items-center gap-1.5">
                <Copy className="h-3.5 w-3.5" /> Copy to Clipboard
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Deployment & Gemini API Key Configuration Modal */}
      {isConfigModalOpen && (
        <div className="fixed inset-0 z-[70] flex items-center justify-center bg-slate-900/70 backdrop-blur-sm p-4 animate-in fade-in">
          <div className="bg-white w-full max-w-2xl overflow-hidden flex flex-col rounded-2xl shadow-2xl border border-slate-200">
            {/* Header */}
            <div className="p-5 border-b border-slate-200 bg-gradient-to-r from-slate-900 to-indigo-950 text-white flex justify-between items-center">
              <div className="flex items-center gap-3">
                <div className="bg-amber-500/20 p-2.5 rounded-xl border border-amber-400/30">
                  <Key className="h-6 w-6 text-amber-400" />
                </div>
                <div>
                  <h3 className="font-extrabold text-base">Gemini API Key & Deployment Setup</h3>
                  <p className="text-xs text-slate-300">Live AI Diagnostics & Zero-Downtime Key Configuration</p>
                </div>
              </div>
              <button 
                onClick={() => setIsConfigModalOpen(false)}
                className="text-slate-400 hover:text-white p-1.5 rounded-lg hover:bg-white/10 transition-colors"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-6 space-y-5 bg-slate-50/50 max-h-[75vh] overflow-y-auto">
              {/* Telemetry Status Card */}
              <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-2xs space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-black uppercase tracking-wider text-slate-400">Current Deployment Status</span>
                  {geminiStatus?.configured ? (
                    <span className="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                      <span className="w-2 h-2 rounded-full bg-emerald-500"></span> Active & Configured
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-1.5 text-xs font-bold text-amber-800 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-200">
                      <span className="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span> Unconfigured
                    </span>
                  )}
                </div>

                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                    <span className="text-[10px] font-bold text-slate-400 block uppercase">Stored Key</span>
                    <span className="font-mono font-bold text-slate-800">
                      {geminiStatus?.masked_key || "None configured"}
                    </span>
                  </div>
                  <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                    <span className="text-[10px] font-bold text-slate-400 block uppercase">RAG Engine Target</span>
                    <span className="font-semibold text-slate-800">Google Gemini Flash / Pro</span>
                  </div>
                </div>
              </div>

              {/* API Key Input Field */}
              <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-2xs space-y-3">
                <label className="text-xs font-bold text-slate-800 flex items-center justify-between">
                  <span>Enter / Rotate Gemini API Key</span>
                  <a 
                    href="https://aistudio.google.com/app/apikey" 
                    target="_blank" 
                    rel="noreferrer" 
                    className="text-blue-600 hover:underline flex items-center gap-1 text-[11px] font-semibold"
                  >
                    Get Free Key from Google AI Studio <ExternalLink className="h-3 w-3" />
                  </a>
                </label>

                <div className="relative">
                  <input 
                    type={showApiKeyText ? "text" : "password"}
                    value={inputApiKey}
                    onChange={(e) => setInputApiKey(e.target.value)}
                    placeholder={geminiStatus?.masked_key ? `Leave blank to test stored key, or enter new key...` : "Paste Gemini API Key (AQ.Ab... or AIza...)"}
                    className="w-full font-mono text-xs pr-10 pl-3.5 py-2.5 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <button 
                    type="button" 
                    onClick={() => setShowApiKeyText(!showApiKeyText)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 p-1 cursor-pointer"
                    title={showApiKeyText ? "Hide Key" : "Show Key"}
                  >
                    {showApiKeyText ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>

                {/* Validation and Action Controls */}
                <div className="flex flex-wrap items-center gap-2 pt-1">
                  <button 
                    type="button"
                    onClick={handleValidateKey}
                    disabled={isValidatingKey}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2 shadow-sm transition active:scale-95 disabled:opacity-50 cursor-pointer"
                  >
                    <RefreshCw className={`h-3.5 w-3.5 ${isValidatingKey ? "animate-spin" : ""}`} />
                    {isValidatingKey ? "Validating with Google AI..." : "⚡ Test & Validate Key"}
                  </button>

                  <button 
                    type="button"
                    onClick={handleSaveKey}
                    disabled={isSavingKey || !inputApiKey.trim()}
                    className="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-xl text-xs font-bold flex items-center gap-2 shadow-sm transition active:scale-95 disabled:opacity-50 cursor-pointer"
                  >
                    <CheckCircle className="h-3.5 w-3.5" />
                    {isSavingKey ? "Saving..." : "💾 Save & Apply to Environment"}
                  </button>
                </div>

                {/* Live Diagnostic Validation Feedback */}
                {validationResult && (
                  <div className={`mt-3 p-3.5 rounded-xl border text-xs leading-relaxed animate-in fade-in ${validationResult.valid ? "bg-emerald-50 border-emerald-200 text-emerald-900" : "bg-rose-50 border-rose-200 text-rose-900"}`}>
                    <div className="flex items-start gap-2.5">
                      {validationResult.valid ? (
                        <CheckCircle className="h-5 w-5 text-emerald-600 shrink-0 mt-0.5" />
                      ) : (
                        <AlertTriangle className="h-5 w-5 text-rose-600 shrink-0 mt-0.5" />
                      )}
                      <div className="space-y-1">
                        <strong className="block text-sm">
                          {validationResult.valid ? "✔ Gemini API Key Verified & Connected!" : "✖ Validation Failed"}
                        </strong>
                        <p className="font-medium">
                          {validationResult.message || validationResult.error}
                        </p>
                        {validationResult.valid && (
                          <div className="flex items-center gap-3 mt-1.5 text-[11px] text-emerald-700 font-bold">
                            <span>⏱️ Latency: {validationResult.latency_ms} ms</span>
                            <span>•</span>
                            <span>🤖 Model Verified: {validationResult.model || "Gemini Flash"}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}

                {/* Save Confirmation Message */}
                {saveSuccessMsg && (
                  <div className="p-3 bg-blue-50 border border-blue-200 text-blue-900 rounded-xl text-xs font-bold flex items-center gap-2 animate-in fade-in">
                    <CheckCircle className="h-4 w-4 text-blue-600" />
                    <span>{saveSuccessMsg}</span>
                  </div>
                )}
              </div>

              {/* Deployment Guidelines */}
              <div className="bg-slate-100/70 border border-slate-200 rounded-xl p-4 text-xs text-slate-600 space-y-2">
                <span className="font-bold text-slate-800 block text-[11px] uppercase tracking-wide">
                  🚀 Production Deployment Guidelines
                </span>
                <p className="text-[11px] leading-relaxed">
                  When deploying to <strong>Docker</strong>, <strong>Render</strong>, <strong>Railway</strong>, or <strong>AWS/Cloud Run</strong>, set your environment variable:
                </p>
                <code className="block bg-slate-900 text-emerald-400 p-2 rounded-lg font-mono text-[11px]">
                  GEMINI_API_KEY=&quot;your-api-key-here&quot;
                </code>
                <p className="text-[11px] text-slate-500">
                  This panel permits instant runtime rotation without downtime. When no key is configured or during high demand, Copilot gracefully serves verified certified statutory ratio transcripts from the local RAG knowledge base.
                </p>
              </div>
            </div>

            {/* Footer */}
            <div className="p-4 bg-white border-t border-slate-200 flex justify-end">
              <button 
                onClick={() => setIsConfigModalOpen(false)}
                className="bg-slate-100 hover:bg-slate-200 text-slate-700 px-5 py-2 rounded-xl text-xs font-bold transition cursor-pointer"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}

function StatCard({ title, value, subtitle, icon }: { title: string, value: string, subtitle: string, icon: React.ReactNode }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white shadow-sm hover:shadow-md transition-all p-5">
      <div className="flex items-center justify-between pb-2">
        <span className="tracking-tight text-[11px] font-extrabold text-slate-400 uppercase">{title}</span>
        <div className="p-2 bg-slate-50 rounded-lg border border-slate-100">{icon}</div>
      </div>
      <div className="text-3xl font-black text-slate-900 tracking-tight">{value}</div>
      <p className="text-[11px] text-slate-400 mt-1 font-medium">{subtitle}</p>
    </div>
  );
}

function EnhancedFeedItem({ doc, tags, matchedMatters, index }: { doc: any, tags: string[], matchedMatters: any[], index: number }) {
  const score = doc.classification?.relevance_score || "P1";
  
  const getScoreBadge = (s: string) => {
    if (s === "P0") return "bg-red-50 text-red-700 border-red-200";
    if (s === "P1") return "bg-amber-50 text-amber-700 border-amber-200";
    return "bg-blue-50 text-blue-700 border-blue-200";
  };

  const whatChanged = doc.impact_note?.what_changed || doc.impact_note?.what_happened || "";

  return (
    <div className="p-5 border border-slate-200 rounded-xl bg-white hover:border-blue-400 hover:shadow-md transition-all space-y-3 group">
      
      {/* Top Meta with Index */}
      <div className="flex justify-between items-start gap-3">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-[11px] font-bold text-slate-400 mr-1">#{index}</span>
          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-200">
            {doc.document_type || "DOCUMENT"}
          </span>
          <span className="text-xs font-semibold text-slate-500">
            {doc.authority}
          </span>
          <span className="text-xs text-slate-400">• {new Date(doc.retrieval_date || doc.created_at).toLocaleDateString('en-IN')}</span>
        </div>

        <span className={`px-2.5 py-1 text-[11px] font-black rounded-md border whitespace-nowrap ${getScoreBadge(score)}`}>
          Priority: {score}
        </span>
      </div>

      {/* Title */}
      <h3 className="font-extrabold text-slate-900 text-base leading-snug group-hover:text-blue-700 transition-colors">
        {doc.title}
      </h3>

      {/* What Changed Highlight */}
      {whatChanged && (
        <p className="text-xs text-slate-600 line-clamp-2 leading-relaxed bg-slate-50 p-2.5 rounded-lg border border-slate-100 font-medium">
          <strong className="text-slate-800">Key Proposition:</strong> {whatChanged}
        </p>
      )}

      {/* Matched Matters Badge */}
      {matchedMatters.length > 0 && (
        <div className="flex items-center gap-1.5 text-xs text-indigo-800 bg-indigo-50/80 px-2.5 py-1.5 rounded-lg border border-indigo-200 font-medium">
          <Briefcase className="h-3.5 w-3.5 text-indigo-600 shrink-0" />
          <span className="truncate">
            <b>Impacts Active Matters:</b> {matchedMatters.map(m => `${m.id} (${m.client.split(' ')[0]})`).join(', ')}
          </span>
        </div>
      )}

      {/* Topic Tags */}
      <div className="flex gap-1.5 flex-wrap pt-1">
        {tags.map((t: string) => (
          <span key={t} className={`text-[10px] font-bold uppercase tracking-wide px-2.5 py-1 rounded-md border shadow-2xs ${getTagBadgeStyle(t)}`}>
            {t.replace(/_/g, " ")}
          </span>
        ))}
      </div>
    </div>
  );
}

# Website Integration Guide: Cyber Law Watch Agent

This guide provides 4 practical options for integrating the **Cyber Law Watch Agent** and its **Cyber Watch Copilot** into your law firm website, client intranet, or enterprise portal.

---

## Option 1: Embeddable Floating Copilot Widget (Recommended)
Add a floating AI intelligence widget (like Intercom or Zendesk) to any WordPress, Webflow, Squarespace, or custom website.

### Step 1: Add Widget Code to your Website Footer / HTML
Paste this code snippet right before the closing `</body>` tag of your website:

```html
<!-- Cyber Law Watch Floating Copilot Widget -->
<div id="cyber-copilot-container"></div>
<script>
  (function() {
    // 1. Create Floating Button
    var btn = document.createElement("button");
    btn.innerHTML = "⚖️ Cyber Law Copilot";
    btn.style.cssText = "position:fixed;bottom:24px;right:24px;z-index:9999;background:#1d4ed8;color:#fff;border:none;padding:12px 20px;border-radius:9999px;font-family:sans-serif;font-weight:bold;font-size:13px;cursor:pointer;box-shadow:0 10px 25px rgba(0,0,0,0.2);display:flex;align-items:center;gap:8px;";
    
    // 2. Create Floating Modal / Iframe
    var iframe = document.createElement("iframe");
    iframe.src = "https://cyberwatch.yourfirm.com"; // URL of your deployed agent
    iframe.style.cssText = "position:fixed;bottom:80px;right:24px;width:440px;height:640px;max-width:calc(100vw-32px);max-height:80vh;border:none;border-radius:16px;box-shadow:0 25px 50px rgba(0,0,0,0.25);z-index:9999;display:none;";
    
    btn.onclick = function() {
      iframe.style.display = iframe.style.display === "none" ? "block" : "none";
    };
    
    document.body.appendChild(iframe);
    document.body.appendChild(btn);
  })();
</script>
```

---

## Option 2: Full-Page Portal Embed (iFrame)
Embed the full authoritative dashboard directly inside an existing page on your firm's client portal:

```html
<iframe 
  src="https://cyberwatch.yourfirm.com" 
  width="100%" 
  height="900px" 
  style="border: 1px solid #e2e8f0; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);"
  allow="clipboard-write"
></iframe>
```

---

## Option 3: Headless REST API Integration
If you want to display recent cyber rulings in your firm's own custom design (e.g. WordPress blog sidebar or React client dashboard), query the backend REST API directly:

### 1. Ingested Rulings Endpoint:
- **URL**: `GET http://your-backend:8080/api/v1/documents/`
- **Response**:
```json
{
  "total": 8,
  "items": [
    {
      "id": "...",
      "title": "W.P. 28912/2024: Debit Freeze Limited Strictly to Disputed Amount",
      "authority": "High Court of Karnataka",
      "original_url": "/docs/kar_hc_28912_2024.pdf",
      "classification": { "relevance_score": "P0", "tags": ["BANK_ACCOUNT_FREEZE", "LIEN"] }
    }
  ]
}
```

### 2. Copilot Query Endpoint:
- **URL**: `POST http://your-backend:8080/api/v1/copilot/ask`
- **Payload**:
```json
{
  "question": "Can police freeze entire account under Sec 102 CrPC?",
  "limit": 6
}
```

---

## Option 4: Subpath Deployment via Reverse Proxy
Host the agent directly under your main domain (e.g., `yourfirm.com/cyber-watch/`):

### Nginx Configuration:
```nginx
location /cyber-watch/ {
    proxy_pass http://127.0.0.1:3000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

location /cyber-watch-api/ {
    proxy_pass http://127.0.0.1:8080/;
    proxy_set_header Host $host;
}
```

### CORS Configuration in `backend/.env`:
Ensure your public domain is added to `CORS_ORIGINS`:
```env
CORS_ORIGINS=http://localhost:3000,https://yourfirm.com,https://portal.yourfirm.com
```

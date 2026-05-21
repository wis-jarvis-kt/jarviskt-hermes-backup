# Annual Statement Retrieval Skill

## Trigger Phrases
- "get annual statement for [name]"
- "annual statement [name] [year]"
- "download annual statement [name] under [agent]"

---

## Overview
Retrieves Life Insurance Premium Statement PDFs from the HLA Agent Portal for any client, under any agent code.

---

## Portal Access
- **URL:** https://portal.hla.com.my/login/default.aspx
- **Login:** ktgoo2880 / PortalKT88-2

---

## Agent Code Hierarchy
- **A0022418** = GOO KAH THART (KT) — Manager level, sees his own clients
- **A0037263** = THAM MAY PENG (May Peng / wife) — Agent level, sees her own clients
- Other agents: A0045264, A0093724, A0104975, A0106586, etc.

**Rule:**
- Each policy belongs to ONE specific agent code
- A policy under A0037263 will NOT appear under A0022418 search (and vice versa)
- Always ask "which agent code?" if not specified
- "KT" or "A0022418" → default, no change needed
- "May Peng" or "A0037263" → must change dropdown first

---

## Step-by-Step Flow

### Step 1: Login
```
Navigate to: https://portal.hla.com.my/login/default.aspx
Fill: txtID = ktgoo2880, txtPassword = PortalKT88-2
Click: btnLogin
Wait: 5 seconds
```

### Step 2: Navigate to Life Insurance Premium Statement
```
Navigate to: https://portal.hla.com.my/cms/Servicing/Policy-Info.aspx
Click link: "Life Insurance Premium Statement"
Wait: 5 seconds
```
> ⚠️ Must go through Policy-Info page — direct URL causes session timeout

### Step 3: Change Agent Code (CRUCIAL — do this FIRST)
```javascript
// Set dropdown value
document.getElementById('cphContent_ddlSearchAgentCode').value = 'A0037263';
// Trigger ASP.NET postback (NOT just .change() event — must use __doPostBack)
__doPostBack('ctl00$cphContent$ddlSearchAgentCode', '')
// Wait for postback to complete
await asyncio.sleep(8)
```
> ⚠️ Must use `__doPostBack()` — simple `.dispatchEvent(new Event('change'))` does NOT work
> ⚠️ Must wait 8 seconds for postback to complete before typing name

### Step 4: Key in Life Assured Name + Year
```javascript
document.getElementById('cphContent_txtLifeAssuredName').value = 'WONG KAR WAI';
document.getElementById('cphContent_cboDUYear').value = '2025'; // or '2024', '2023', '' for View All
```

### Step 5: Get Record
```javascript
document.getElementById('cphContent_btnGetRec').click()
// Wait 6 seconds
```

### Step 6: Extract PDF URLs
```javascript
// Get all PDF links with policy numbers
Array.from(document.querySelectorAll('tr')).map(r => {
    var link = r.querySelector('a[id*="Hyperlink1"]');
    var cells = r.querySelectorAll('td');
    return link ? {policy: cells[2].innerText.trim(), url: link.href} : null;
}).filter(Boolean)
```

### Step 7: Download PDF using curl (NOT Page.printToPDF)
```bash
curl -k -L -o output.pdf \
  -H "Cookie: <session_cookies>" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Referer: https://portal.hla.com.my/LifeInsurancePremium/WebUI/LifeInsurancePremiumSearch.aspx" \
  "<pdf_url>"
```
> ⚠️ Use `curl -k` (skip SSL verification — HLA uses self-signed cert)
> ⚠️ Do NOT use `Page.printToPDF` — that screenshots the page, not the real PDF
> ✅ Real PDF starts with `%PDF-1.7` header, ~320-330KB per file

### Step 8: Get Session Cookies via CDP
```python
await send("Network.enable", {})
cookies_raw = await send("Network.getCookies", {"urls": ["https://portal.hla.com.my"]})
cookies = cookies_raw["result"]["cookies"]
cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
```

---

## File Naming Convention
```
2025_AnnStmt_<FULL_NAME_UNDERSCORED>_<POLICY_NO>.pdf
```
Example: `2025_AnnStmt_WONG_KAR_WAI_UL202528294172.pdf`

---

## Save Location
```
~/.openclaw/workspace/annual_statements/
```

---

## Chrome Setup (CDP Headless)
```python
proc = subprocess.Popen([
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--remote-debugging-port=9223",
    "--remote-allow-origins=*",
    "--user-data-dir=/tmp/hla-chrome-profile",
    "--no-first-run", "--no-default-browser-check",
    "--disable-extensions", "--headless=new",
    "https://portal.hla.com.my/login/default.aspx"
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
```

---

## Common Mistakes to Avoid
| ❌ Wrong | ✅ Correct |
|---|---|
| Navigate directly to LIPS URL | Go through Policy-Info page first |
| Use `.dispatchEvent(new Event('change'))` for agent dropdown | Use `__doPostBack()` |
| Type name BEFORE changing agent code | Change agent code FIRST, wait 8s, THEN type name |
| Use `Page.printToPDF` to save | Use `curl -k` with session cookies |
| Assume same results under both agent codes | Each policy belongs to ONE agent code only |

---

## Policy Enquiry (finding all policies for a client)
Same flow but navigate to **Policy Enquiry** instead:
```
Click: "Policy Enquiry" link on Policy-Info page
Change agent code via __doPostBack (same as above)
Select radio: cphContent_radMyOpt5 (Life Assured Name)
Type name: cphContent_txtSearchLifeAssuredName
Click: cphContent_btnGetRec
```

---

## Script
Full implementation: `scripts/hla_portal.py`
- `get_annual_statement()` method handles full flow
- Uses CDP + curl for reliable PDF download

---

## Notes
- HLA portal session expires ~2 min — always re-login fresh
- UL2025xxx new policies may not have annual statements yet (generated yearly)
- Wong Kar Wai family example: 6 policies under A0022418, 1 active under A0037263
- AW YEONG YEE MEI: 1 new policy under A0037263 (UL202528295152)
- WONG JING CHUI: 2 new policies under A0037263 (UL202528296633, UL202528297086)

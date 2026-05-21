#!/usr/bin/env python3
"""
HLA: Download 2025 Life Insurance Premium Statements
Correct path: Login -> Servicing -> Policy Info -> Life Insurance Premium Statement
For: GANENDRA (Agent A0022418 / KT)
"""
import asyncio, base64, json, os, ssl, subprocess, time, urllib.request, websockets

PORT = 9250  # Reuse existing Chrome on port 9250
USERNAME = "ktgoo2880"
PASSWORD = "PortalKT88-3"
OUTPUT_DIR = os.path.expanduser("~/WisSend")
HLA_LOGIN = "https://portal.hla.com.my/login/default.aspx"
HLA_POLICY_INFO = "https://portal.hla.com.my/cms/Servicing/Policy-Info.aspx"

SEARCHES = [
    ("FAM KIM CHOY", "A0022418", "2025"),
]


def get_tab_id():
    resp = urllib.request.urlopen(f"http://localhost:{PORT}/json/list", timeout=5)
    tabs = [t for t in json.loads(resp.read()) if t.get("type") == "page"]
    if not tabs:
        raise RuntimeError("No page tab found")
    return tabs[0]["id"]


async def cdp_connect(tab_id):
    return await websockets.connect(
        f"ws://localhost:{PORT}/devtools/page/{tab_id}",
        ping_interval=None, max_size=50 * 1024 * 1024)


class CDP:
    def __init__(self, ws):
        self.ws = ws
        self._id = 1

    async def send(self, method, params=None, timeout=60):
        mid = self._id; self._id += 1
        await self.ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(await asyncio.wait_for(self.ws.recv(), timeout=timeout))
            if msg.get("id") == mid:
                return msg

    async def eval(self, expr, timeout=60):
        r = await self.send("Runtime.evaluate", {"expression": expr, "awaitPromise": True}, timeout=timeout)
        return r.get("result", {}).get("result", {}).get("value")

    async def navigate(self, url, wait=5):
        await self.send("Page.navigate", {"url": url})
        await asyncio.sleep(wait)

    async def wait_load(self, extra=2):
        for _ in range(15):
            if await self.eval("document.readyState") == "complete":
                break
            await asyncio.sleep(1)
        await asyncio.sleep(extra)

    async def get_cookies(self):
        r = await self.send("Network.getCookies")
        return r.get("result", {}).get("cookies", [])

    async def print_to_pdf(self):
        r = await self.send("Page.printToPDF", {
            "printBackground": True, "paperWidth": 8.27, "paperHeight": 11.69,
            "marginTop": 0.3, "marginBottom": 0.3, "marginLeft": 0.3, "marginRight": 0.3
        }, timeout=30)
        return r.get("result", {}).get("data", "")


async def login(cdp):
    await cdp.navigate(HLA_LOGIN, wait=8)
    await cdp.wait_load(2)
    await cdp.eval(
        f"document.getElementById('txtID').value='{USERNAME}';"
        f"document.getElementById('txtPassword').value='{PASSWORD}';"
    )
    await cdp.eval("document.getElementById('btnLogin').click()")
    await asyncio.sleep(7)
    await cdp.wait_load(2)
    url = await cdp.eval("window.location.href")
    print(f"Logged in: {url}")
    return url


async def get_stmt_url(cdp):
    """Navigate to Policy Info page and extract Life Insurance Premium Statement URL."""
    await cdp.navigate(HLA_POLICY_INFO, wait=7)
    await cdp.wait_load(2)
    url = await cdp.eval(
        "(function(){"
        "var links=Array.from(document.querySelectorAll('a'));"
        "var l=links.find(function(a){return a.innerText&&a.innerText.trim()==='Life Insurance Premium Statement';});"
        "return l?l.href:null;"
        "})()"
    )
    print(f"Stmt page URL: {url}")
    return url


async def ensure_session(cdp, stmt_url):
    """Check session is alive, re-login and get fresh stmt_url if needed."""
    await cdp.navigate(stmt_url, wait=7)
    await cdp.wait_load(3)
    cur = await cdp.eval("window.location.href")
    body = await cdp.eval("document.body.innerText")
    if 'timeout' in (cur or '').lower() or 'login' in (cur or '').lower() or 'SESSION TIMED' in (body or ''):
        print("  Session expired, re-logging in...")
        await login(cdp)
        stmt_url = await get_stmt_url(cdp)
        await cdp.navigate(stmt_url, wait=7)
        await cdp.wait_load(3)
    return stmt_url


async def fill_and_search(cdp, la_name, agent, year):
    """Fill form fields and click search."""
    form_els = await cdp.eval(
        "JSON.stringify(Array.from(document.querySelectorAll('select,input')).map(function(el){"
        "return {tag:el.tagName,id:el.id,name:el.name,type:el.type||'',"
        "opts:el.tagName==='SELECT'?Array.from(el.options).map(function(o){return o.value+':'+o.text;}):[]"
        "};}).filter(function(el){return el.id||el.name;}))"
    )
    els = json.loads(form_els or '[]')
    print(f"  Fields: {[e['id'] or e['name'] for e in els if e['tag'] in ('SELECT','INPUT') and e['type'] != 'hidden']}")

    # Set agent dropdown
    for el in els:
        if el['tag'] == 'SELECT' and 'agent' in (el['id'] + el['name']).lower():
            r = await cdp.eval(
                f"(function(){{"
                f"var dd=document.getElementById('{el['id']}');"
                f"if(!dd)return 'no dd';"
                f"var o=Array.from(dd.options).find(function(o){{return o.value==='{agent}'||o.text.includes('{agent}');}});"
                f"if(!o)return 'not found,opts:'+Array.from(dd.options).map(function(o){{return o.value;}}).join(',');"
                f"dd.value=o.value;dd.dispatchEvent(new Event('change'));return 'ok:'+dd.value;"
                f"}})()"
            )
            print(f"  Agent: {r}")
            await asyncio.sleep(2)
            break

    # Set life assured name
    for el in els:
        combined = (el['id'] + el['name']).lower()
        if el['tag'] == 'INPUT' and el['type'] != 'hidden' and (
                'lifeassured' in combined or ('life' in combined and 'name' in combined) or 'assured' in combined):
            r = await cdp.eval(
                f"(function(){{"
                f"var inp=document.getElementById('{el['id']}');"
                f"if(!inp)return 'no inp';"
                f"inp.value='{la_name}';"
                f"inp.dispatchEvent(new Event('input'));inp.dispatchEvent(new Event('change'));"
                f"return 'ok:'+inp.value;"
                f"}})()"
            )
            print(f"  Name: {r}")
            await asyncio.sleep(1)
            break

    # Set year
    for el in els:
        if el['tag'] == 'SELECT' and 'year' in (el['id'] + el['name']).lower():
            r = await cdp.eval(
                f"(function(){{"
                f"var dd=document.getElementById('{el['id']}');"
                f"if(!dd)return 'no dd';"
                f"var o=Array.from(dd.options).find(function(o){{return o.value==='{year}'||o.text==='{year}';}});"
                f"if(!o)return 'not found,opts:'+Array.from(dd.options).map(function(o){{return o.value;}}).join(',');"
                f"dd.value=o.value;dd.dispatchEvent(new Event('change'));return 'ok:'+dd.value;"
                f"}})()"
            )
            print(f"  Year: {r}")
            await asyncio.sleep(1)
            break

    # Click search button
    r = await cdp.eval(
        "(function(){"
        "var btns=Array.from(document.querySelectorAll('input[type=submit],input[type=button],button'));"
        "var b=btns.find(function(b){var t=(b.value||b.innerText||'').toLowerCase();"
        "return t.includes('get')||t.includes('search')||t.includes('record');});"
        "if(b){b.click();return 'clicked:'+(b.value||b.innerText||'btn');}"
        "return 'not found:'+btns.slice(0,5).map(function(b){return b.value||b.innerText;}).join(',');"
        "})()"
    )
    print(f"  Search btn: {r}")
    await asyncio.sleep(8)
    await cdp.wait_load(3)


async def download_results(cdp, la_name, agent, year, stmt_url, output_dir):
    """Find ViewPdf links in results and download each."""
    result_text = await cdp.eval("document.body.innerText")
    print(f"  Result preview: {(result_text or '')[:150]}")

    rows_raw = await cdp.eval(
        "JSON.stringify(Array.from(document.querySelectorAll('tr')).map(function(tr){"
        "var cells=Array.from(tr.querySelectorAll('td')).map(function(td){return td.innerText.trim();});"
        "var links=Array.from(tr.querySelectorAll('a')).map(function(a){return {text:a.innerText.trim(),href:a.href};});"
        "return {cells:cells,links:links};"
        "}).filter(function(r){return r.links.some(function(l){return l.text.toLowerCase()==='viewpdf';});}))"
    )
    rows = json.loads(rows_raw or '[]')
    print(f"  ViewPdf rows: {len(rows)}")

    cookies = await cdp.get_cookies()
    cookie_str = '; '.join([f"{c['name']}={c['value']}" for c in cookies])
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE

    agent_tag = "KT" if agent == "A0022418" else "THAM"

    downloaded = []
    for row in rows:
        pdf_link = next((l for l in row['links'] if l['text'].lower() == 'viewpdf'), None)
        if not pdf_link:
            continue
        policy_no = next((c for c in row['cells'] if c.startswith('UL') or c.startswith('TL')), 'unknown')
        href = pdf_link['href']
        fname = f"{la_name.replace(' ', '_')}_{agent_tag}_{policy_no}_{year}.pdf"
        fpath = os.path.join(output_dir, fname)
        print(f"  → {policy_no}: {href[:80]}")
        try:
            req = urllib.request.Request(href, headers={
                "Cookie": cookie_str, "User-Agent": "Mozilla/5.0",
                "Accept": "application/pdf,*/*", "Referer": stmt_url
            })
            with urllib.request.urlopen(req, timeout=60, context=ssl_ctx) as resp:
                data = resp.read()
            if b'%PDF' in data[:100]:
                with open(fpath, 'wb') as f:
                    f.write(data)
                print(f"    ✅ {fname} ({len(data):,}b)")
                downloaded.append(fname)
            else:
                # Open in browser and print to PDF
                print(f"    Not PDF ({len(data)}b) — printing from browser...")
                await cdp.navigate(href, wait=8)
                await cdp.wait_load(3)
                pdf_data = await cdp.print_to_pdf()
                if pdf_data:
                    with open(fpath, 'wb') as f:
                        f.write(base64.b64decode(pdf_data))
                    print(f"    📄 {fname} ({os.path.getsize(fpath):,}b)")
                    downloaded.append(fname)
                # Return to stmt page for next iteration
                await cdp.navigate(stmt_url, wait=5)
                await cdp.wait_load(2)
        except Exception as e:
            print(f"    ❌ {e}")
    return downloaded


async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output: {OUTPUT_DIR}")

    tab_id = get_tab_id()
    ws = await cdp_connect(tab_id)
    cdp = CDP(ws)
    await cdp.send("Page.enable")
    await cdp.send("Network.enable")

    all_downloaded = []

    # Login and get stmt URL
    cur = await cdp.eval("window.location.href")
    if 'login' in (cur or '').lower() or 'timeout' in (cur or '').lower():
        await login(cdp)
    else:
        print(f"Already at: {cur}")

    stmt_url = await get_stmt_url(cdp)
    if not stmt_url:
        print("ERROR: Could not find Life Insurance Premium Statement link — re-logging in")
        await login(cdp)
        stmt_url = await get_stmt_url(cdp)

    for la_name, agent, year in SEARCHES:
        print(f"\n{'='*55}")
        print(f"{la_name} | {agent} | {year}")
        try:
            stmt_url = await ensure_session(cdp, stmt_url)
            await fill_and_search(cdp, la_name, agent, year)
            files = await download_results(cdp, la_name, agent, year, stmt_url, OUTPUT_DIR)
            all_downloaded.extend(files)
            if not files:
                print(f"  ⚠️  No PDFs found for {la_name}/{agent}")
        except Exception as e:
            print(f"  ERROR: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'='*55}")
    print(f"COMPLETE — {len(all_downloaded)} files downloaded:")
    for f in all_downloaded:
        print(f"  {f}")

    await ws.close()


if __name__ == "__main__":
    asyncio.run(main())

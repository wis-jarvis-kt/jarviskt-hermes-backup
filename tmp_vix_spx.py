import urllib.request
import urllib.error
import json

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}

# ── VIX ──────────────────────────────────────────────────────────────────────────
try:
    vix_url = 'https://query2.finance.yahoo.com/v8/finance/chart/%5EVIX?interval=1d&range=1d'
    req = urllib.request.Request(vix_url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        vix_data = json.loads(r.read())
    vix = vix_data['chart']['result'][0]['meta']['regularMarketPrice']
    print(f"VIX: {vix:.2f}")
except Exception as e:
    print(f"VIX error: {e}")

# ── S&P 500 ────────────────────────────────────────────────────────────────────────
try:
    spx_url = 'https://query2.finance.yahoo.com/v8/finance/chart/%5EGSPC?interval=1d&range=5d'
    req2 = urllib.request.Request(spx_url, headers=headers)
    with urllib.request.urlopen(req2, timeout=15) as r2:
        spx_data = json.loads(r2.read())
    spx_meta = spx_data['chart']['result'][0]['meta']
    spx = spx_meta['regularMarketPrice']
    prev = spx_meta.get('chartPreviousClose') or spx_meta.get('previousClose')
    print(f"S&P 500: ${spx:.2f}  prevClose: ${prev}")
    if prev:
        pct = (spx - prev) / prev * 100
        print(f"S&P change: {pct:+.2f}%")
    else:
        print("S&P prevClose: N/A")
except Exception as e:
    print(f"S&P error: {e}")

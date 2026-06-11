# ETF CSP Analysis — Reusable Workflow

## Quick-Run Script Pattern

For scheduled CSP analysis runs, write the Python fetch script to a file, then execute via `terminal`. This avoids the `<<` heredoc background-process guard in foreground mode.

```python
# Saved to: ~/.hermes/hermes-agent/etf_analysis.py
import urllib.request, json

# Fetch Fear & Greed
with urllib.request.urlopen("https://api.alternative.me/fng/", timeout=10) as r:
    fng = json.loads(r.read())['data'][0]
    fng_val = int(fng['value'])

# Fetch S&P (5d to handle missing previousClose)
url = "https://query2.finance.yahoo.com/v8/finance/chart/%5EGSPC?interval=1d&range=5d"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
data = json.loads(urllib.request.urlopen(req).read())
closes = [c for c in data['chart']['result'][0]['indicators']['quote'][0]['close'] if c]
sp_price = closes[-1]
sp_prev = closes[-2]
sp_change = ((sp_price - sp_prev) / sp_prev) * 100

# Fetch VIX
url = "https://query2.finance.yahoo.com/v8/finance/chart/%5EVIX?interval=1d&range=1d"
...
```

Run: `python3 ~/.hermes/hermes-agent/etf_analysis.py`

## ETF Prices — Latest Snapshot

| Symbol | Price | Notes |
|--------|-------|-------|
| SPYM | $85.77 | |
| SCHG | $32.93 | |
| DYNF | $65.30 | |
| CGGR | $44.81 | |
| SPHQ | $85.32 | |
| XLG | $60.64 | |
| AIQ | $62.08 | |
| SOXQ | $99.99 | High IV candidate |
| PSI | $154.58 | |

*Snapshot from 2026-06-11 run. Do not use stale — refresh each run.*

## WhatsApp Delivery (Cron Jobs)

Format: `hermes send -t "whatsapp:56702359580792@lid" "message text"`

Verify LID first: `hermes send --list whatsapp`
DMs show as `whatsapp:Goo Kah Thart  [56702359580792@lid]`
Use the LID portion (without `whatsapp:` prefix) as the target.
---
name: openclaw-stock-analysis-victor-framework
description: Victor framework for CSP (Cash Secured Put) and CC (Covered Call) analysis on ETFs. Fetches market data, applies Victor's rules, and formats reports.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [stock, trading, options, CSP, covered-call, ETF, Victor-framework, market-analysis]
prerequisites:
  commands: [python3, curl]
---

# Stock Analysis — Victor CSP/CC Framework

Apply Victor's rules for selling Cash Secured Puts (CSP) and Covered Calls (CC) on ETFs.

## Victor's Rules

- **Sell PUT on RED days**: S&P down >1%, IV >40%, Fear & Greed <25
- **Sell CALL on GREEN days**: S&P up >1%
- **Wait for RED day = better premiums** — do NOT force trades when conditions aren't met

RED day = ideal PUT sell entry. GREEN day = CC opportunity. VIX above 20 + Extreme Fear = maximum PUT premium zone.

## Workflow

1. Fetch data via Python3 + urllib (NOT curl|pipe to python — blocked by security scan):
   - Fear & Greed: `https://api.alternative.me/fng/`
   - S&P 500: `https://query2.finance.yahoo.com/v8/finance/chart/%5EGSPC?interval=1d&range=1d`
   - VIX: `https://query2.finance.yahoo.com/v8/finance/chart/%5EVIX?interval=1d&range=1d`
   - ETF prices: `https://query2.finance.yahoo.com/v8/finance/chart/{TICKER}?interval=1d&range=1d`

2. Write Python script to `/Users/ktoclaw/.hermes/tmp/etf_analysis.py` first, then run it.

3. Add `User-Agent` header to avoid Yahoo Finance 429s:
   ```python
   req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"})
   ```

4. Parse responses:
   - `meta.regularMarketPrice` — current price
   - `meta.chartPreviousClose` — previous close (NOT `previousClose` which may not exist for indices)
   - SPX change %: `((regularMarketPrice - chartPreviousClose) / chartPreviousClose) * 100`

5. Apply Victor conditions to determine today's verdict.

6. Deliver report via appropriate channel (WhatsApp, Telegram, etc.) — NOT iMessage from cron jobs (see imessage skill).

## Key ETFs to Track

SPYM (dividend/quality), SCHG (growth), DYNF (dynamic factor), CGGR (quality/growth), SPHQ (quality), XLG (large cap growth), AIQ (AI/global), SOXQ (semiconductors), PSI (digital payments).

## Verdict Logic

| Condition | PUT (RED day) | CALL (GREEN day) |
|-----------|--------------|-----------------|
| S&P change | <-1% | >+1% |
| VIX | >20 (ideally >25) | any |
| Fear & Greed | <25 (Extreme Fear) | >75 (Extreme Greed) |
| IV | >40% | any |

Today's data → verdict → waitlist of top 4 ETF candidates → entry triggers.

## Support Files

- `references/2026-06-03-session.md` — session log with market data snapshot and key learnings

## Pitfalls

### Yahoo Finance Rate Limiting (429)
Yahoo Finance aggressively rate-limits without a proper User-Agent. Always include a realistic UA header. If you get a 429, wait and retry withUA. Never pipe curl to python — use Python file + subprocess or Python's urllib directly.

### SPX Previous Close Key
For S&P 500 and VIX, the previous close is stored as `chartPreviousClose`, NOT `previousClose`. The latter may be absent on index data.

### Cron Job Delivery
iMessage (imsg) requires Full Disk Access to ~/Library/Messages/chat.db and a GUI session. Cron jobs run headless and will fail with `permissionDenied`. Use platform messaging (Telegram, WhatsApp, Discord) for automated delivery from cron jobs.

## Output Format

Keep reports WhatsApp-friendly:
- Bullet points, no markdown tables
- Brief market conditions (S&P, VIX, FNG)
- Today's verdict with trigger checkmarks
- Key ETF prices inline
- Waitlist of 4 candidates
- Entry trigger conditions
- If not a PUT day: suggest CALL strategy
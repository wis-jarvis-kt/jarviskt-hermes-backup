---
name: openclaw-stock-analysis-victor-framework
description: |
  [ARCHIVED - Absorbed into `stock-analysis-victor-framework`]
  This skill was a CSP/CC-only wrapper that has been superseded by the full
  `stock-analysis-victor-framework` skill at:
  `~/.hermes/skills/openclaw/stock-analysis-victor-framework/SKILL.md`

  Note: The canonical skill is at `openclaw/stock-analysis-victor-framework/` (NOT `openclaw/openclaw-stock-analysis-victor-framework/`).

  The canonical skill includes: Victor Entry Signals (P/E + PEG vs 5Y avg),
  Stock Radar (daily), Weekly Victor Study, CSP screening, and news scanning.
  All CSP-specific content is preserved inline in the canonical skill.

  Do NOT use this skill for new work — reference `stock-analysis-victor-framework` instead.
version: 1.0.0
status: archived
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [stock, trading, options, CSP, covered-call, ETF, Victor-framework, market-analysis]
    absorbed_into: stock-analysis-victor-framework
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

2. Write Python script to `~/.hermes/etf_csp_analysis.py` first, then run it via `python3`. Do NOT pipe curl to python (blocked by security scan).

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

### SPX/VIX Previous Close — Use Indicators Array, Not Meta Keys
For S&P 500 and VIX, both `previousClose` AND `chartPreviousClose` may be absent from `meta`. The reliable approach:
1. Parse `indicators.quote[0].close` — it's an array with possible None values
2. Filter to valid closes: `[c for c in closes if c is not None]`
3. Current price = `regularMarketPrice` (always valid)
4. Previous close = `valid_closes[-2]` (second-to-last valid value)

```python
def get_prev_close(data):
    closes = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    valid_closes = [c for c in closes if c is not None]
    return valid_closes[-2]  # previous close
```

Meta keys `previousClose` and `chartPreviousClose` are unreliable for indices — the indicators array approach is the robust default.

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
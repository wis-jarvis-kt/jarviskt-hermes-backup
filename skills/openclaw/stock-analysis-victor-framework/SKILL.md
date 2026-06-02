---
name: stock-analysis-victor-framework
category: openclaw
description: Analyze stocks using Victor's framework (PEG vs 5Y avg, P/E vs 5Y avg) and CNN Fear & Greed index for entry points.
---

## Overview
This skill provides a structured approach to analyze selected stocks for potential entry points using Victor's framework, which compares current P/E and PEG ratios against their 5-year averages. It also incorporates the CNN Fear & Greed Index to gauge overall market sentiment.

> **Reference:** See `references/stock-radar.md` for the watchlist, data source URLs, and quick-reference ratios.

## Steps
1.  **Get Current Date:** Obtain the current date in YYYY-MM-DD format using `terminal("date +%Y-%m-%d")`.
2.  **Check CNN Fear & Greed Index:**
    *   **Preferred:** Use `delegate_task` with web tool to fetch the index value (fastest, most reliable).
    *   **Fallback:** `browser_navigate` to CNN Fear & Greed page — the page is dynamic and often times out or blocks curl scraping; do not rely on curl/grep against `money.cnn.com`.
    *   **Proxy if unavailable:** Use VIX as sentiment proxy. VIX < 15 = Extreme Greed/Neutral; 15-20 = Neutral; >25 = Fear. Record "unavailable — using VIX [N] as proxy" in the report.
3.  **Analyze Each Stock (e.g., AAPL, NVDA, META, GOOGL, MSFT, TSLA):**
    > **Preferred data source: `yfinance` via `terminal` + Python** — faster and more reliable than browser scraping Yahoo Finance for valuation data. Browser navigation is the fallback for deep-dive or when yfinance is insufficient.

    a. **Pull current data via yfinance (terminal):**
       ```python
       import yfinance as yf
       t = yf.Ticker(sym)
       info = t.info
       price = info.get('regularMarketPrice') or info.get('currentPrice')
       trailing_pe = info.get('trailingPE')
       forward_pe = info.get('forwardPE')
       peg_ratio = info.get('pegRatio')
       shares = info.get('sharesOutstanding', 0)
       ```
    b. **Compute 5Y average P/E from historical data:**
       *   Get annual net income: `t.financials.loc['Net Income']` (last 4-5 years)
       *   Get historical year-end prices: `t.history(period='5y')` → `resample('YE').last()['Close']`
       *   Compute annual EPS = net_income / shares_outstanding
       *   Historical P/E per year = year-end price / annual EPS
       *   5Y Avg P/E = mean of available annual P/Es (need ≥3 years for meaningful avg)
    c. **Apply Victor's Framework:**
       *   **P/E Comparison:** `Current P/E < 5Y Avg P/E × 0.90` → P/E entry signal ✅
       *   **PEG Comparison:** `Current PEG < 1.0` → Peter Lynch bargain zone (standalone strong signal); `Current PEG < 5Y Avg PEG × 0.90` → PEG entry signal ✅
       *   **Strong entry:** Both conditions met. **Potential entry:** Either condition met.
    d. **If yfinance is insufficient:** Fall back to `browser_navigate("https://finance.yahoo.com/quote/{SYM}/statistics")` → snapshot → scroll → parse "Valuation Measures" section for Trailing P/E and PEG Ratio.

## Computing 5Y Avg P/E — Worked Example (NVDA)

> **Note on shares outstanding:** Required to convert total net income to per-share EPS for historical P/E calculation. Yahoo Finance `info.sharesOutstanding` provides this. Do not skip — without it, historical P/E cannot be computed.

**Preferred approach: use `scripts/stock_radar_pe.py`** — it handles the year-end close indexing and scalar conversion correctly. Run it via:
```bash
python3 ~/.hermes/skills/openclaw/stock-analysis-victor-framework/scripts/stock_radar_pe.py [SYMBOL ...]
```
Defaults to AAPL, NVDA, META, GOOGL, MSFT, TSLA.

```python
t = yf.Ticker('NVDA')
info = t.info
price = info.get('regularMarketPrice')  # 217.93
shares = info.get('sharesOutstanding', 0)  # 24.221e9

# Annual net income (FY ends Jan)
financials = t.financials  # has Net Income rows
# earnings_by_year = financials.loc['Net Income']  # index = dates

# Historical year-end closes
hist = t.history(period='5y')
yearly_closes = hist.resample('YE').last()['Close']
# e.g. 2022: 14.60, 2023: 49.49, 2024: 134.25, 2025: 186.49

# Annual EPS = Net Income / shares
# NI 2022 = 4.37B → EPS = 4.37e9 / 24.221e9 = 0.18
# NI 2025 = 120.07B → EPS = 120.07e9 / 24.221e9 = 4.96

# Historical P/Es: 2022: 14.60/0.18=81, 2023: 49.49/1.23=40, ...
# 5Y Avg P/E = mean([81, 40, 45, 38]) = 51.0
# Current P/E 33.4 → 33.4 < 51.0 × 0.90 = 45.9 → ✅ P/E entry signal
```

## CSP (Sell Put) Screening — 2-Stage Protocol

When Master KT asks for "etf put analysis", "sell put candidates", "check IV", or "CSP screen":

### Stage 1 — Volume Screen
```python
# Use terminal + Python (execute_code sandbox lacks yfinance)
# Yahoo Finance requires User-Agent header to avoid 429:
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
import yfinance as yf
etfs = ['SPYM','SCHG','DYNF','CGGR','SPHQ','XLG','AIQ','SOXQ','PSI']
for sym in etfs:
    t = yf.Ticker(sym)
    info = t.info
    price = info.get('regularMarketPrice') or info.get('currentPrice')
    vol = info.get('averageVolume') or 0
    print(f"{sym}: ${price:.2f}, Vol: {vol/1e6:.1f}M")
```
Pass = Vol > 1M. Failed ones are removed from consideration.

### Stage 2 — IV Check (at RED day trigger ONLY)
```python
import yfinance as yf
t = yf.Ticker(sym)
expires = list(t.options)
opt = t.option_chain(expires[0])
puts = opt.puts
puts['dist'] = abs(puts['strike'] - price)
atm = puts.loc[puts['dist'].idxmin()]
iv = atm['impliedVolatility'] * 100
roi = (atm['lastPrice'] / (atm['strike'] * 100)) * 100
```
Pass = IV > 40% AND S&P >1% down on that day. Only then is CSP entry justified.

### CSP RED Day Trigger — VIX Proxy
- S&P drop >1% in a day (today's -0.22% is MARGINAL/FLAT, NOT RED)
- VIX spike above 20 (low VIX = thin premiums)
- Fear & Greed <25 (extreme fear zone)

**When Fear & Greed is unavailable (CNN blocking):** Use VIX as proxy.
- VIX < 15 → Extreme Greed / Neutral (no CSP)
- VIX 15-20 → Neutral (marginal premiums, most ETFs fail Stage 2)
- VIX > 25 → Fear zone → Stage 2 justified

Record in report: `"Fear & Greed: unavailable — VIX [N] = [label]"` so reader knows the gap.

### Top CSP Candidates (as of 2026-06-02 — refresh monthly)
1. SOXQ — consistently highest IV among semiconductors; re-check before each run
2. FNDX, AIQ, XLG — check IV > 40% threshold on RED days only

**Do NOT use stale data.** The CSP candidates above reflect May 21 conditions and may be outdated. Always run the Volume Screen (Stage 1) and IV Check (Stage 2) fresh before each CSP analysis.

### Key Lessons
- VIX below 20 = low IV everywhere, most ETFs fail Stage 2
- SOXQ consistently highest IV among semiconductors
- Low-volume ETFs (TMFC, USMC, SNPE) never pass Stage 1 — don't waste time on them
- Market is only "RED" when S&P drops >1% — -0.22% is marginal/flat

> **Full screening data:** `references/stock-radar.md`

## News Scanning (Lightweight)
For quick multi-company news scanning without browser navigation, use Google News RSS:
```
https://news.google.com/rss/search?q={COMPANY}+stock&hl=en-US&gl=US&ceid=US:en
```
Loop with `curl -s "<url>" | grep -o '<title>[^<]*</title>' | head -5` for fast headlines across multiple companies.
Avoids rate-limiting issues with web search — more reliable for batch queries.

## Victor's 5 Sectors — Company Watchlists

| Sector | Companies |
|--------|-----------|
| AI/ML | NVDA, MSFT, GOOGL, AMZN, META |
| Semiconductors | NVDA, TSM, AVGO, AMD, SSNLF |
| Cloud | AMZN (AWS), MSFT (Azure), GOOGL (GCP), BABA (Alibaba Cloud), ORCL (OCI) |
| E-Commerce | AMZN, WMT, SHOP, PDD, BABA |
| Cybersecurity | PANW, CRWD, FTNT, ZS, MSFT (Defender) |

---

## Weekly Victor Study (Cron Job)

A weekly recurring cron job that produces a structured sector deep-dive across Victor's 5 watchlist sectors, saving to `~/.hermes/memories/victor-study-YYYY-MM-DD.md`.

### Trigger Conditions
- Run weekly (MEMORY.md: "Weekly sector deep-dives")
- NOT triggered by ad-hoc single-sector requests — those use this skill directly

### Workflow

**Step 1 — Check Prior Outputs (before doing any new searches)**

Read these files to avoid redundant fetches:
1. `stock-radar-YYYY-MM-DD.md` — for today's P/E, PEG, Fear & Greed, and entry signals
2. `research-YYYY-MM-DD.md` — for today's news developments from research-scout
3. `victor-study-YYYY-MM-DD.md` — prior day's study for carryover context (prices, key facts)
4. `research-YYYY-MM-DD.md` for any new sector-relevant news from that day

**Step 2 — Identify Gaps**

After reading above, determine what's genuinely new vs. carryover:
- Prices, P/E, PEG → from stock-radar (already fetched today)
- Major news/earnings announcements → from research-scout (already captured today)
- Company-specific stock moves, analyst actions since yesterday → need subagent search

**Step 3 — Launch Subagent Waves (supplemental only)**

If gaps exist, use the batch pattern (see `delegate_task` batching below):
- Wave 1: AI/ML + Semiconductors + Cloud (3 tasks, max_concurrent_children=3)
- Wave 2: E-Commerce + Cybersecurity (2 tasks)
- Each task: one sector's worth of companies, bullet summaries, "NEW since [date]" focus
- Do NOT re-fetch what was already captured in Steps 1-2

**Step 4 — Compile victor-study-YYYY-MM-DD.md**

Use this section structure:

```
## AI & Machine Learning
## Semiconductors
## Cloud Computing
## E-Commerce
## Cybersecurity
```

Each section: 5 companies, bullet format, inline source citations pointing to stock-radar/research files.

**Add a "NEW" subsection** when research-scout or subagents surfaced something genuinely new to that sector today (e.g., regulatory guidance, product announcement, analyst action not in prior day's study).

**Step 5 — Verify**

Read back first few lines to confirm file wrote correctly and last section is complete.

### Output Format

```markdown
# Victor Company Study — YYYY-MM-DD

## AI & Machine Learning
- **NVDA** — ...

## Semiconductors
...

## Cloud Computing
...

## E-Commerce
...

## Cybersecurity
...

---
*Generated by Hermes cron job — victor-study-YYYY-MM-DD.md*
*Prior studies: victor-study-YYYY-MM-DD-2, victor-study-YYYY-MM-DD-1*
```

### delegate_task Batching Pattern (for multi-sector research)

For structured multi-company research (5 sectors × 5 companies = 25 tickers), batch by **sector** into waves of ≤ 3 tasks. Each subagent handles one sector's worth of companies in a single call — far more efficient than one subagent per company.

`max_concurrent_children = 3` is the hard limit. Plan waves accordingly:

```
Wave 1 (3 sectors): AI/ML, Semiconductors, Cloud
Wave 2 (2 sectors): E-Commerce, Cybersecurity
```

Each subagent prompt should:
- State all 5 companies explicitly in the prompt
- Ask for a concise bullet summary per company, not raw JSON
- Include "Focus on what's NEW since [prior study date]" to avoid duplicating yesterday's data

Validated: 2026-05-29 session ran 3 waves (3+3+3 tasks) for Victor Study with no anti-bot failures.

## Pitfalls
*   **execute_code sandbox lacks yfinance AND has urllib quirks:** Always use `terminal` with Python scripts for market data fetching. `execute_code` does not have yfinance installed. Also avoid `hermes send` heredoc syntax via `<<` in terminal foreground mode — it triggers the background-process guard. Write the message to a file first, then use `hermes send --file /path/to/file`.
*   **S&P previousClose may be N/A in Yahoo Finance chart meta:** When `meta.regularMarketPrice` exists but `previousClose` is N/A, fetch the 5-day price series to calculate the actual % change. Use: `url = "...?interval=1d&range=5d"` → parse `indicators.quote[0].close` timestamps with `datetime.fromtimestamp(t)`.
*   **hermes send WhatsApp target format:** Must be `whatsapp:56702359580792@lid` — prefix `whatsapp:` is required, and the @lid suffix identifies the specific contact. Use `hermes send --list` to enumerate all available targets first.
*   **CNN Fear & Greed blocks curl/grep:** Do not attempt to scrape `money.cnn.com` with curl. The page returns empty grep results. Use `https://api.alternative.me/fng/` which returns JSON directly — reliable, no browser needed.
*   **web_search unavailability:** If `web_search` is not available as a tool, use `browser_navigate` for initial information gathering (e.g., for CNN Fear & Greed Index) instead of a direct search API.
*   **Incomplete Historical Data:** Yahoo Finance may not always provide 5 full years (20 quarters) of quarterly data directly on the statistics page. Approximate averages from available data and clearly state if data is inconclusive (e.g., N/A if less than 3 quarters are available or if data is entirely missing).
*   **Dynamic Page Content:** Yahoo Finance pages are dynamic. Multiple `browser_scroll` and `browser_snapshot` calls may be needed to ensure all data is captured, especially within the "Statistics" section which can be quite long. Target specific sections by looking for headings like "Valuation Measures".
*   **Batch news with RSS:** Google News RSS is faster than browser for multi-company scans but returns only titles + snippets. Use it for headlines, not deep research.
*   **Shares outstanding required for historical P/E:** Without `info['sharesOutstanding']`, net income cannot be converted to per-share EPS for historical P/E computation fails. Always pull shares first.
*   **Year-end close Series/indexing bug:** When computing annual P/Es from `hist.resample('YE').last()['Close']`, the result is a Series indexed by datetime. Accessing via string year (`closes_df[year_str]`) can return a Series rather than a scalar if the index doesn't match exactly. **Fix:** After `resample('YE').last()`, iterate with positional `.iloc[i]` or build a dict with `{idx.year: float(val)}` loop — never assume `df[str(year)]` returns a scalar. Test with `isinstance(val, (int, float))` before using.
*   **Scalar conversion for numpy/pandas types:** When comparing P/E values (trailing_pe, avg_pe), ensure they are plain Python floats before arithmetic — use `float(x)` explicitly on each value. Comparing pandas scalars directly (e.g. `trailing_pe < avg_pe * 0.90`) raises `ValueError: The truth value of a Series is ambiguous`. Cast every extracted value to `float()` before arithmetic or boolean comparison.
*   **Delivering reports to WhatsApp groups via bridge:** The Hermes `send_message` tool fails for WhatsApp groups with error `Cannot destructure property 'user' of 'jidDecode(...)' as it is undefined` — a gateway adapter bug when routing group JIDs. **Workaround:** Use `terminal` with Python/curl to call the bridge directly:
    ```python
    import urllib.request, json
    url = "http://127.0.0.1:3000/send"
    payload = {"chatId": "120363423080731840@g.us", "message": "..."}
    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        print(r.read().decode())
    ```
    Bridge must be running (`curl http://127.0.0.1:3000/health` → `{"status":"connected"}`). Group JID format = `120363423080731840@g.us` (not the `whatsapp:` prefix format used by Hermes send CLI). Verified working 2026-06-01.
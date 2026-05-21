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
    *   Navigate to the CNN Fear & Greed Index page using `browser_navigate(url="https://money.cnn.com/data/fear-and-greed/")`.
    *   Take a full snapshot with `browser_snapshot(full=True)` and parse the current index value and sentiment.
3.  **Analyze Each Stock (e.g., AAPL, NVDA, META, GOOGL, MSFT, TSLA):**
    *   For each stock in the target list:
        a.  **Navigate to Yahoo Finance Statistics Page:** Construct the Yahoo Finance URL (e.g., `https://finance.yahoo.com/quote/AAPL/statistics`) and navigate using `browser_navigate`.
        b.  **Extract Valuation Measures:**
            *   Take a full browser snapshot `browser_snapshot(full=True)`.
            *   Scroll down (`browser_scroll(direction='down')` and take more snapshots if needed) until the "Valuation Measures" section is visible.
            *   Extract "Trailing P/E" (Current P/E) and "PEG Ratio (5yr expected)" (Current PEG) from the current column.
            *   Extract quarterly historical P/E and PEG ratios from the table under "Valuation Measures" for the last 5 available quarters (columns titled with dates like "3/31/2026", "12/31/2025", etc.).
        c.  **Calculate/Approximate 5-Year Averages:**
            *   If direct 5-year averages are not available, approximate by averaging the available quarterly data (up to 5 quarters) for both P/E and PEG from the extracted historical data.
        d.  **Apply Victor's Framework:**
            *   **P/E Comparison:** Check if `Current P/E` is at least 10% below its approximate `5Y Avg P/E`.
            *   **PEG Comparison:** Check if `Current PEG` is at least 10% below its approximate `5Y Avg PEG`.
            *   A stock is considered a "Potential Entry Point" if either condition is met. A "Strong Potential Entry Point" if both are met.
4.  **Compile Report:** Summarize the findings for each stock, including current prices, P/E, PEG, 5Y averages, and the verdict based on Victor's framework. Include the CNN Fear & Greed Index.
5.  **Save Report:** Write the compiled report to a Markdown file at `~/.hermes/memories/stock-radar-YYYY-MM-DD.md` using `write_file`.

## CSP (Sell Put) Screening — 2-Stage Protocol

When Master KT asks for "etf put analysis", "sell put candidates", "check IV", or "CSP screen":

### Stage 1 — Volume Screen
```python
import yfinance as yf
etfs = ['AIQ','SOXQ','SCHG','DYNF','CGGR','SPHQ','XLG','SPYM','FNDX','FDVV','TDIV','PSI','IETC','USMC','SNPE','TMFC','FLQL','WTV']
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

### RED Day Criteria
- S&P drop >1% in a day (today's -0.22% is MARGINAL/FLAT, NOT RED)
- VIX spike above 20 (low VIX = thin premiums)
- Fear & Greed <25 (extreme fear zone)

### Top CSP Candidates (May 21, 2026 screen — SOXQ leads)
1. SOXQ — IV 51.7%, premium $6.90, ROI 7.3%/mo
2. FNDX — IV 50.0%, premium $1.20, ROI 4.3%/mo
3. AIQ — IV 43.2%, ROI 3.1%/mo
4. XLG — IV 43.7%, ROI 1.6%/mo

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

## Pitfalls
*   **`web_search` unavailability:** If `web_search` is not available as a tool, use `browser_navigate` for initial information gathering (e.g., for CNN Fear & Greed Index) instead of a direct search API.
*   **Incomplete Historical Data:** Yahoo Finance may not always provide 5 full years (20 quarters) of quarterly data directly on the statistics page. Approximate averages from available data and clearly state if data is inconclusive (e.g., N/A if less than 3 quarters are available or if data is entirely missing).
*   **Dynamic Page Content:** Yahoo Finance pages are dynamic. Multiple `browser_scroll` and `browser_snapshot` calls may be needed to ensure all data is captured, especially within the "Statistics" section which can be quite long. Target specific sections by looking for headings like "Valuation Measures".
*   **Batch news with RSS:** Google News RSS is faster than browser for multi-company scans but returns only titles + snippets. Use it for headlines, not deep research.
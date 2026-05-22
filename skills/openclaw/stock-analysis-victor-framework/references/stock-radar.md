# Stock Radar — Reference Data

## Stocks Under Coverage

Primary watchlist (from cron job `hermes-stock-radar-945pm`):
`AAPL`, `NVDA`, `META`, `GOOGL`, `MSFT`, `TSLA`

## Key Data Sources

| Source | URL Pattern | Data Needed | Reliability |
|--------|-------------|-------------|-------------|
| Yahoo Finance Statistics | `https://finance.yahoo.com/quote/{SYMBOL}/statistics` | Trailing P/E, PEG Ratio (5yr expected), quarterly historical | Browser only, slow |
| **yfinance (terminal/Python)** | `import yfinance as yf` | Price, P/E, PEG, fundamentals, historical prices | ✅ **Preferred** |
| CNN Fear & Greed Index | `https://money.cnn.com/data/fear-and-greed/` | Current index value + sentiment | Blocks curl; use delegate_task or VIX proxy |
| Morningstar | `https://www.morningstar.com/stocks/{symbol}/valuation` (approx) | P/E, P/B, P/S, PEG vs 5Y avg | Browser only |
| Dataroma | `https://dataroma.com/` | What billionaire investors actually hold | Browser only |
| Finviz | `https://finviz.com/quote.ashx?ty=c&p=d&b=1` | Stock screener | Browser only |

## Victor's Framework — Quick Reference

**Entry signal (either condition met = potential entry):**
- Current P/E ≥ 10% below 5Y average P/E
- Current PEG ≥ 10% below 5Y average PEG

**Strong entry signal (both conditions met):**
- Current P/E ≥ 10% below 5Y average P/E **AND**
- Current PEG ≥ 10% below 5Y average PEG

**PEG < 1 standalone:** Peter Lynch bargain zone — strong signal even if not below 5Y avg.

**Fear & Greed interpretation:**
- 0-25: Extreme Fear → buying opportunity
- 25-45: Fear → potentially good entry
- 45-55: Neutral
- 55-75: Greed → be cautious on new buys
- 75-100: Extreme Greed → don't buy

**When Fear & Greed is unavailable (CNN blocks scraping):** Use VIX as proxy:
- VIX < 15 → Extreme Greed/Neutral
- VIX 15-20 → Neutral (most ETFs fail CSP Stage 2 in this range)
- VIX > 25 → Fear zone → CSP Stage 2 justified

## Valuation Ratios Cheat Sheet

| Ratio | Best For | Signal |
|-------|----------|--------|
| P/E | Large profitable companies | Compare vs 5yr avg |
| P/B | Banks, real estate, manufacturers | <1 = below asset value |
| P/S ⭐ | Tech, unprofitable companies | Victor's favourite |
| PEG | Profitable growth companies | <1 = bargain (Peter Lynch) |

## Cron Job

- **Job ID:** `505bb59fcf82`
- **Schedule:** `45 21 * * 1-5` (9:45 PM weekdays)
- **Last run:** 2026-05-22 21:00 ✅
- **Output file:** `memories/stock-radar-YYYY-MM-DD.md`

## Key Lessons Learned (2026-05-22)

- **yfinance via terminal is the preferred data source** — faster and more reliable than browser scraping. Use `terminal` with Python for all yfinance calls.
- **execute_code sandbox does NOT have yfinance installed** — modules installed via `pip3 install` in terminal are not available in execute_code. Always use `terminal` for yfinance work.
- **CNN Fear & Greed blocks curl scraping** — do not attempt grep against `money.cnn.com`. Use `delegate_task` with web tool, or fall back to VIX proxy.
- **Historical P/E calculation requires shares outstanding** — `t.info['sharesOutstanding']` is needed to convert total net income to per-share EPS for annual P/E computation.
- **5Y avg P/E needs ≥3 years of data** — if fewer than 3 annual data points available, note "insufficient data for 5Y avg" and use forward P/E as proxy.
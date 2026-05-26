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

## ETF Watchlist (CSP Candidates)

Primary ETFs tracked for CSP (Cash Secured Put) analysis:
`SPYM`, `SCHG`, `DYNF`, `CGGR`, `SPHQ`, `XLG`, `AIQ`, `SOXQ`, `PSI`

Secondary/niche ETFs (may fail Stage 1 volume screen):
`FNDX`, `FDVV`, `TDIV`, `IETC`, `USMC`, `SNPE`, `TMFC`, `FLQL`, `WTV`

## Data Fetching Patterns

### Yahoo Finance REST API (preferred for prices/VIX/S&P)
Requires `User-Agent` header to avoid 429 rate limiting:
```python
import urllib.request, json
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=15) as r:
    data = json.loads(r.read())
```
URLs:
- S&P 500: `https://query2.finance.yahoo.com/v8/finance/chart/%5EGSPC?interval=1d&range=1d`
- VIX: `https://query2.finance.yahoo.com/v8/finance/chart/%5EVIX?interval=1d&range=1d`
- ETF price: `https://query2.finance.yahoo.com/v8/finance/chart/{SYMBOL}?interval=1d&range=1d`

Extract price: `data['chart']['result'][0]['meta']['regularMarketPrice']`
Extract previous close: `data['chart']['result'][0]['meta']['chartPreviousClose']`

### Fear & Greed Index
- API (no header needed): `https://api.alternative.me/fng/`
- Extract: `data['data'][0]['value']` (int string) and `data['data'][0]['value_classification']`

### yfinance (for option chains and fundamentals — terminal only)
```python
import yfinance as yf
t = yf.Ticker(sym)
info = t.info  # price, P/E, PEG, volume
options = list(t.options)  # available expiration dates
opt = t.option_chain(options[0])
puts = opt.puts  # strike, lastPrice, impliedVolatility
```
Note: `execute_code` sandbox does NOT have yfinance — use `terminal` with Python for yfinance calls.

## Cron Job

- **Schedule:** `30m before market close` (e.g. `0 15 * * 1-5`) or morning run `0 9 * * 1-5`
- Output: deliver report to configured home channel

## Key Lessons Learned (2026-05-22)

- **yfinance via terminal is the preferred data source** — faster and more reliable than browser scraping. Use `terminal` with Python for all yfinance calls.
- **execute_code sandbox does NOT have yfinance installed** — modules installed via `pip3 install` in terminal are not available in execute_code. Always use `terminal` for yfinance work.
- **CNN Fear & Greed blocks curl scraping** — do not attempt grep against `money.cnn.com`. Use `delegate_task` with web tool, or fall back to VIX proxy.
- **Historical P/E calculation requires shares outstanding** — `t.info['sharesOutstanding']` is needed to convert total net income to per-share EPS for annual P/E computation.
- **5Y avg P/E needs ≥3 years of data** — if fewer than 3 annual data points available, note "insufficient data for 5Y avg" and use forward P/E as proxy.
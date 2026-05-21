# Stock Analysis Reference — Victor Framework

## Stocks Under Coverage

Primary watchlist (from cron job `hermes-stock-radar-945pm`):
`AAPL`, `NVDA`, `META`, `GOOGL`, `MSFT`, `TSLA`

## Key Data Sources

| Source | URL Pattern | Data Needed |
|--------|-------------|-------------|
| Yahoo Finance Statistics | `https://finance.yahoo.com/quote/{SYMBOL}/statistics` | Trailing P/E, PEG Ratio (5yr expected), quarterly historical |
| CNN Fear & Greed Index | `https://money.cnn.com/data/fear-and-greed/` | Current index value + sentiment |
| Morningstar | `https://www.morningstar.com/stocks/{symbol}/valuation` (approx) | P/E, P/B, P/S, PEG vs 5Y avg |
| Dataroma | `https://dataroma.com/` | What billionaire investors actually hold |
| Finviz | `https://finviz.com/quote.ashx?ty=c&p=d&b=1` | Stock screener |

## Victor's Framework — Quick Reference

**Entry signal (either condition met = potential entry):**
- Current P/E ≥ 10% below 5Y average P/E
- Current PEG ≥ 10% below 5Y average PEG

**Strong entry signal (both conditions met):**
- Current P/E ≥ 10% below 5Y average P/E **AND**
- Current PEG ≥ 10% below 5Y average PEG

**Fear & Greed interpretation:**
- 0-25: Extreme Fear → buying opportunity
- 25-45: Fear → potentially good entry
- 45-55: Neutral
- 55-75: Greed → be cautious on new buys
- 75-100: Extreme Greed → don't buy

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
- **Last run:** 2026-05-20 21:49
- **Output file:** `memories/stock-radar-YYYY-MM-DD.md`
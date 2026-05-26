# ETF CSP Screening Reference

> Session data: May 21, 2026. Updated when IV screening is re-run.

## How to Run CSP Screening (2-Stage Protocol)

### Stage 1 — Volume Screen (Daily, Low Cost)
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

**Pass:** Vol > 1M → qualifies for Stage 2 at trigger time.

### Stage 2 — IV Check (At RED Day Trigger)
```python
import yfinance as yf

# For each volume-passing ETF at trigger time:
t = yf.Ticker(sym)
expires = list(t.options)
opt = t.option_chain(expires[0])
puts = opt.puts
puts['dist'] = abs(puts['strike'] - price)
atm = puts.loc[puts['dist'].idxmin()]
iv = atm['impliedVolatility'] * 100
premium = atm['lastPrice']
strike = atm['strike']
roi = (premium / (strike * 100)) * 100  # cash secured is strike * 100 per contract
```

**Pass:** IV > 40% AND on RED day (S&P >1% down).

---

## May 21, 2026 Screening Results

### Market Context
- S&P 500: 7,416 (-0.22% 🔴) — NOT a RED day (>1% needed)
- VIX: 17.40 (low IV environment)
- Fear & Greed: 29 (Fear, not extreme)

### Volume Pass List (9 of 18)
| ETF | Price | Volume | Pass? |
|-----|-------|--------|-------|
| AIQ | $62.00 | 1.7M | ✓ |
| SOXQ | $93.77 | 2.1M | ✓ |
| SCHG | $34.20 | 8.5M | ✓ |
| DYNF | $66.29 | 2.2M | ✓ |
| CGGR | $45.88 | 2.4M | ✓ |
| SPHQ | $83.07 | 2.0M | ✓ |
| XLG | $63.33 | 1.9M | ✓ |
| SPYM | $87.09 | 7.4M | ✓ |
| FNDX | $30.41 | 2.7M | ✓ |

**Failed:** TDIV, PSI, IETC, USMC, SNPE, TMFC, FLQL, FDVV, WTV (all below 1M vol)

### IV Screen on Volume-Passed ETFs
| ETF | ATM Strike | IV | Pass? | Premium | Monthly ROI* |
|-----|-----------|-----|-------|---------|-------------|
| AIQ | $62.00 | 43.2% | ✓ | $1.92 | 3.1% |
| SOXQ | $95.00 | 51.7% | ✓ | $6.90 | 7.3% |
| XLG | $63.00 | 43.7% | ✓ | $1.02 | 1.6% |
| FNDX | $28.00 | 50.0% | ✓ | $1.20 | 4.3% |
| SCHG | $34.00 | 22.0% | ✗ | — | — |
| DYNF | $60.00 | 6.3% | ✗ | — | — |
| CGGR | $46.00 | 0.0% | ✗ | — | — |
| SPHQ | $83.00 | 0.4% | ✗ | — | — |
| SPYM | $87.00 | 0.2% | ✗ | — | — |

*ROI = premium / (strike × 100) per month. Cash secured = strike × 100 per contract.

### Top CSP Candidates (for when RED day triggers)
1. **SOXQ** — IV 51.7%, premium $6.90, best ROI at 7.3%/mo
2. **FNDX** — IV 50.0%, premium $1.20, solid 4.3%/mo
3. **AIQ** — IV 43.2%, marginal pass, 3.1%/mo
4. **XLG** — IV 43.7%, marginal pass, 1.6%/mo (lower premium)

### Key Lessons
- VIX below 20 = low IV everywhere, most ETFs fail IV screen
- SOXQ consistently has highest IV among semiconductors
- Low-volume ETFs (TMFC, USMC, SNPE) never pass Stage 1
- ROI calculation: (premium / cash_secured) × 100 per month
  - Cash secured = strike × 100 per contract
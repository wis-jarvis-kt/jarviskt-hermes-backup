import yfinance as yf
import urllib.request
import json
import math

stocks = ['AAPL', 'NVDA', 'META', 'GOOGL', 'MSFT', 'TSLA']

# ── 1. CNN Fear & Greed ──────────────────────────────────────────
try:
    req = urllib.request.Request('https://api.alternative.me/fng/', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as r:
        fg = json.loads(r.read())
    fear_greed_value = int(fg['data'][0]['value'])
    fear_greed_class = fg['data'][0]['value_classification']
except Exception as e:
    fear_greed_value = None
    fear_greed_class = f'unavailable – {e}'

print(f"Fear & Greed: {fear_greed_value} ({fear_greed_class})")

# ── 2. Per-stock analysis ─────────────────────────────────────────
results = {}
annual_pes_dict = {}

for sym in stocks:
    try:
        t = yf.Ticker(sym)
        info = t.info
        price = info.get('regularMarketPrice') or info.get('currentPrice')
        trailing_pe = info.get('trailingPE')
        forward_pe = info.get('forwardPE')
        peg_ratio = info.get('pegRatio')
        shares = info.get('sharesOutstanding', 0)

        # 5Y avg P/E via historical year-end prices + annual net income
        hist = t.history(period='5y')
        yearly_closes = hist['Close'].resample('YE').last() if not hist.empty else None

        try:
            financials = t.financials
            if financials is not None and 'Net Income' in financials.index:
                ni_series = financials.loc['Net Income'].dropna()
            else:
                ni_series = None
        except Exception:
            ni_series = None

        avg_pe_5y = None
        annual_pes = []
        avail_years = []

        if yearly_closes is not None and ni_series is not None and shares and shares > 0:
            for dt, close in yearly_closes.items():
                year = dt.year
                matching_ni = ni_series[ni_series.index.map(lambda x: x.year) == year]
                if not matching_ni.empty:
                    ni = float(matching_ni.iloc[0])
                    eps = ni / shares
                    if eps > 0:
                        p_e = close / eps
                        annual_pes.append(p_e)
                        avail_years.append(year)
            if len(annual_pes) >= 3:
                avg_pe_5y = sum(annual_pes) / len(annual_pes)

        results[sym] = {
            'price': price,
            'trailing_pe': trailing_pe,
            'forward_pe': forward_pe,
            'peg_ratio': peg_ratio,
            'shares': shares,
            'avg_pe_5y': avg_pe_5y,
        }
        annual_pes_dict[sym] = list(zip(avail_years, annual_pes)) if annual_pes else []
    except Exception as e:
        results[sym] = {'error': str(e)}
        annual_pes_dict[sym] = []

for sym, d in results.items():
    print(f"\n=== {sym} ===")
    if 'error' in d:
        print(f"  ERROR: {d['error']}")
        continue
    p = d['price']
    tpe = d['trailing_pe']
    fpe = d['forward_pe']
    peg = d['peg_ratio']
    sh = d['shares']
    avg5 = d['avg_pe_5y']
    ap = annual_pes_dict[sym]

    print(f"  Price:        ${p:.2f}" if p else "  Price:        N/A")
    print(f"  Trailing P/E: {tpe:.2f}" if tpe else "  Trailing P/E: N/A")
    print(f"  Forward P/E:  {fpe:.2f}" if fpe else "  Forward P/E:  N/A")
    print(f"  PEG Ratio:    {peg:.2f}" if peg else "  PEG Ratio:    N/A")
    print(f"  Shares:       {sh/1e9:.2f}B" if sh else "  Shares:       N/A")
    print(f"  5Y Avg P/E:  {avg5:.2f}" if avg5 else "  5Y Avg P/E:  N/A")
    if ap:
        print(f"  Annual P/Es:  {ap}")

print("\nDONE")

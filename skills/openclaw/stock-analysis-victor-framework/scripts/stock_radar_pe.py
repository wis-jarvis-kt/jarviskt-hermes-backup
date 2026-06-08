#!/usr/bin/env python3
"""Stock Radar - Victor's Framework Analysis (fixed)"""
import yfinance as yf
import json
from datetime import date

SYMBS = ['AAPL', 'NVDA', 'META', 'GOOGL', 'MSFT', 'TSLA']

# Fear & Greed
try:
    import urllib.request
    req = urllib.request.Request('https://api.alternative.me/fng/', headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as r:
        fg = json.loads(r.read())
    fng_val = fg['data'][0]['value']
    fng_class = fg['data'][0]['value_classification']
    print(f"FEAR_GREED:{fng_val}|{fng_class}")
except Exception as e:
    print(f"FEAR_GREED:error:{e}")

today = date.today().strftime('%Y-%m-%d')
print(f"DATE:{today}")

for sym in SYMBS:
    try:
        t = yf.Ticker(sym)
        info = t.info
        price = info.get('regularMarketPrice') or info.get('currentPrice')
        trailing_pe = info.get('trailingPE')
        peg = info.get('pegRatio')
        shares = info.get('sharesOutstanding', 0)

        # Historical year-end closes
        hist = t.history(period='5y')
        ye = hist.resample('YE').last()['Close']
        # Build dict: {year: close}
        close_by_year = {}
        for dt, v in ye.items():
            close_by_year[int(dt.year)] = float(v)

        # Net income by year — align by column order (most recent first)
        financials = t.financials
        if not financials.empty and 'Net Income' in financials.index:
            ni_row = financials.loc['Net Income']
            cols = list(ni_row.index)  # columns are dates, most recent last
            # Map col years to NI values (most recent 5)
            ni_by_year = {}
            for col in reversed(cols[-5:]):
                yr = int(col.year)
                ni_by_year[yr] = float(ni_row[col])
        else:
            ni_by_year = {}

        # Compute annual P/E where both exist
        years = sorted(set(list(close_by_year.keys()) + list(ni_by_year.keys())))
        pe_list = []
        for yr in years:
            if yr in close_by_year and yr in ni_by_year and shares > 0:
                eps = ni_by_year[yr] / float(shares)
                if eps > 0:
                    pe_list.append((yr, close_by_year[yr], eps, close_by_year[yr] / eps))

        avg_pe = sum(p[3] for p in pe_list) / len(pe_list) if len(pe_list) >= 2 else None

        pe_signal = False
        if trailing_pe and avg_pe:
            pe_signal = float(trailing_pe) < float(avg_pe) * 0.90

        peg_signal = peg is not None and float(peg) < 1.0

        pe_str = f"{trailing_pe:.2f}" if trailing_pe else "N/A"
        peg_str = f"{peg:.2f}" if peg else "N/A"
        avg_str = f"{avg_pe:.2f}" if avg_pe else "N/A"
        pe_sig_str = "YES" if pe_signal else "no"
        peg_sig_str = "YES" if peg_signal else "no"

        print(f"{sym}:price={price:.2f}|trailing_pe={pe_str}|peg={peg_str}|5y_avg_pe={avg_str}|pe_entry={pe_sig_str}|peg_entry={peg_sig_str}|years={len(pe_list)}")
    except Exception as e:
        import traceback
        print(f"{sym}:error:{e}")
        traceback.print_exc()
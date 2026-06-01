#!/usr/bin/env python3
"""
stock_radar_pe.py — Compute 5Y avg P/E and Victor framework entry signals for a list of stocks.
Usage: python3 stock_radar_pe.py [SYMBOL ...]
Defaults to: AAPL NVDA META GOOGL MSFT TSLA
"""
import yfinance as yf
import json
import sys

DEFAULT_STOCKS = ['AAPL', 'NVDA', 'META', 'GOOGL', 'MSFT', 'TSLA']

def compute_annual_pes(ticker_sym):
    """Compute annual P/E ratios from 5Y history. Returns (annual_pes_dict, avg_5y_pe)."""
    t = yf.Ticker(ticker_sym)
    info = t.info
    shares = info.get('sharesOutstanding', 0)
    
    if not shares or shares == 0:
        return {}, None
    
    # Year-end closes: resample to year-end, get last close of each year
    hist = t.history(period='5y')
    yearly_closes = hist.resample('YE').last()['Close']
    
    # Build {year: close_price} dict from the Series
    close_dict = {}
    yearly_closes_list = yearly_closes.sort_index()  # oldest first
    for i, (idx, val) in enumerate(yearly_closes_list.items()):
        close_dict[idx.year] = float(val)
    
    # Annual net income
    financials = t.financials
    net_income = financials.loc['Net Income'] if 'Net Income' in financials.index else None
    
    annual_pes = {}
    if net_income is not None:
        ni_series = net_income.sort_index()  # oldest first
        for date_idx in ni_series.index:
            year = date_idx.year
            if year in close_dict:
                year_close = close_dict[year]
                year_ni = float(ni_series[date_idx])
                annual_eps = year_ni / shares
                if annual_eps > 0:
                    pe = year_close / annual_eps
                    annual_pes[year] = round(pe, 1)
    
    if len(annual_pes) >= 1:
        avg_pe = round(float(sum(annual_pes.values()) / len(annual_pes)), 1)
    else:
        avg_pe = None
    
    return annual_pes, avg_pe

def analyze_stock(ticker_sym):
    """Full Victor framework analysis for one stock."""
    t = yf.Ticker(ticker_sym)
    info = t.info
    
    price = info.get('regularMarketPrice') or info.get('currentPrice')
    trailing_pe_raw = info.get('trailingPE')
    forward_pe_raw = info.get('forwardPE')
    peg_ratio_raw = info.get('pegRatio')
    shares = info.get('sharesOutstanding', 0)
    
    # Cast to plain Python floats to avoid pandas scalar ambiguity in arithmetic
    trailing_pe = float(trailing_pe_raw) if trailing_pe_raw is not None else None
    forward_pe = float(forward_pe_raw) if forward_pe_raw is not None else None
    peg_ratio = float(peg_ratio_raw) if peg_ratio_raw is not None else None
    
    annual_pes, avg_pe = compute_annual_pes(ticker_sym)
    
    pe_threshold = round(avg_pe * 0.90, 1) if avg_pe else None
    pe_signal = bool(trailing_pe < avg_pe * 0.90) if (avg_pe and trailing_pe) else False
    peg_signal = bool(peg_ratio < 1.0) if peg_ratio is not None else False
    
    verdict = "No Entry"
    if pe_signal and peg_signal:
        verdict = "Strong Entry"
    elif pe_signal or peg_signal:
        verdict = "Potential Entry"
    
    return {
        'price': price,
        'trailing_pe': round(trailing_pe, 1) if trailing_pe else None,
        'forward_pe': round(forward_pe, 1) if forward_pe else None,
        'peg_ratio': round(peg_ratio, 2) if peg_ratio else None,
        'annual_pes': annual_pes,
        'avg_5y_pe': avg_pe,
        'pe_threshold_90': pe_threshold,
        'pe_entry_signal': pe_signal,
        'peg_entry_signal': peg_signal,
        'verdict': verdict,
    }

def main():
    stocks = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_STOCKS
    
    results = {}
    for sym in stocks:
        try:
            results[sym] = analyze_stock(sym)
            d = results[sym]
            print(f"\n{sym}: price=${d['price']}, PE={d['trailing_pe']}, PEG={d['peg_ratio']}")
            print(f"  annual_pes={d['annual_pes']}, 5Y_avg_PE={d['avg_5y_pe']}")
            print(f"  P/E signal={d['pe_entry_signal']}, PEG signal={d['peg_entry_signal']} → {d['verdict']}")
        except Exception as e:
            results[sym] = {'error': str(e)}
            print(f"\n{sym}: ERROR {e}")
    
    print("\n\n=== JSON ===")
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
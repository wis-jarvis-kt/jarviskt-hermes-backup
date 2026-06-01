import yfinance as yf
import json

stocks = ['AAPL', 'NVDA', 'META', 'GOOGL', 'MSFT', 'TSLA']
results = {}

for sym in stocks:
    t = yf.Ticker(sym)
    info = t.info
    price = info.get('regularMarketPrice') or info.get('currentPrice')
    trailing_pe = info.get('trailingPE')
    forward_pe = info.get('forwardPE')
    peg_ratio = info.get('pegRatio')
    shares = info.get('sharesOutstanding', 0)
    
    # Historical year-end closes
    hist = t.history(period='5y')
    yearly_closes = hist.resample('YE').last()['Close']
    
    # Annual net income
    financials = t.financials
    net_income = financials.loc['Net Income'] if 'Net Income' in financials.index else None
    
    annual_pes = {}
    if net_income is not None and shares and shares > 0:
        ni_df = net_income.sort_index()  # oldest first
        
        # Build dict of year -> close price
        close_dict = {}
        for idx in yearly_closes.index:
            year = idx.year
            val = yearly_closes.iloc[list(yearly_closes.index).index(idx)]
            if isinstance(val, (int, float)):
                close_dict[year] = float(val)
        
        for date_idx in ni_df.index:
            year = date_idx.year
            if year in close_dict:
                year_close = close_dict[year]
                year_ni = float(ni_df[date_idx])
                annual_eps = year_ni / shares
                if annual_eps > 0:
                    pe = year_close / annual_eps
                    annual_pes[year] = round(pe, 1)
    
    # Compute 5Y avg P/E (scalar)
    if len(annual_pes) >= 1:
        avg_pe = round(float(sum(annual_pes.values()) / len(annual_pes)), 1)
    else:
        avg_pe = None
    
    # Ensure scalar
    trailing_pe_val = float(trailing_pe) if trailing_pe is not None else None
    forward_pe_val = float(forward_pe) if forward_pe is not None else None
    peg_ratio_val = float(peg_ratio) if peg_ratio is not None else None
    
    # Entry signals
    pe_signal = False
    peg_signal = False
    
    if avg_pe is not None and trailing_pe_val is not None:
        pe_signal = trailing_pe_val < (avg_pe * 0.90)
    
    if peg_ratio_val is not None:
        peg_signal = peg_ratio_val < 1.0
    
    results[sym] = {
        'price': price,
        'trailing_pe': round(trailing_pe_val, 1) if trailing_pe_val else None,
        'forward_pe': round(forward_pe_val, 1) if forward_pe_val else None,
        'peg_ratio': round(peg_ratio_val, 2) if peg_ratio_val else None,
        'shares': shares,
        'annual_pes': annual_pes,
        'avg_5y_pe': avg_pe,
        'pe_threshold_90': round(avg_pe * 0.90, 1) if avg_pe else None,
        'pe_entry_signal': pe_signal,
        'peg_entry_signal': peg_signal,
    }

# Print summary
for sym, d in results.items():
    print(f"\n{sym}: price=${d['price']}, PE={d['trailing_pe']}, PEG={d['peg_ratio']}")
    print(f"  annual_pes={d['annual_pes']}, 5Y_avg_PE={d['avg_5y_pe']}")
    print(f"  P/E signal={d['pe_entry_signal']}, PEG signal={d['peg_entry_signal']}")

print("\n\n=== JSON ===")
print(json.dumps(results, indent=2))
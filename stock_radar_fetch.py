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
    results[sym] = {
        'price': price,
        'trailing_pe': trailing_pe,
        'forward_pe': forward_pe,
        'peg_ratio': peg_ratio,
        'shares': shares
    }
    print(f"{sym}: price={price}, PE={trailing_pe}, fwdPE={forward_pe}, PEG={peg_ratio}, shares={shares}")

print("\n--- JSON ---")
print(json.dumps(results, indent=2))
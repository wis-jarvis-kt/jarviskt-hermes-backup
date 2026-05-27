import yfinance as yf
import json
import urllib.request

# Check VIX and S&P
vix = yf.Ticker("^VIX").info.get('regularMarketPrice', 'N/A')
spx = yf.Ticker("^SPX").info
spx_price = spx.get('regularMarketPrice', 'N/A')
spx_prev = spx.get('previousClose', 'N/A')

if spx_price != 'N/A' and spx_prev != 'N/A':
    spx_change = ((spx_price - spx_prev) / spx_prev) * 100
else:
    spx_change = 'N/A'

print(f"VIX: {vix}")
print(f"SPX: {spx_price} (prev: {spx_prev})")
print(f"SPX change: {spx_change}%")

# Fear & Greed
try:
    req = urllib.request.urlopen('https://api.alternative.me/fng/', timeout=5)
    fg = json.loads(req.read())
    fg_value = fg['data'][0]['value']
    fg_class = fg['data'][0]['value_classification']
    print(f"Fear & Greed: {fg_value} ({fg_class})")
except Exception as e:
    print(f"Fear & Greed: unavailable - {e}")

# ETF prices and changes
etfs = ['AIQ', 'SOXQ', 'XLG', 'FNDX']
for sym in etfs:
    t = yf.Ticker(sym)
    info = t.info
    price = info.get('regularMarketPrice') or info.get('currentPrice')
    prev = info.get('previousClose', 'N/A')
    if price and prev and prev != 'N/A':
        chg = ((price - prev) / prev) * 100
        print(f"{sym}: ${price:.2f} ({chg:+.2f}%)")
    else:
        print(f"{sym}: ${price}")
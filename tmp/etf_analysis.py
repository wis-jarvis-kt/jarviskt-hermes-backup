import urllib.request
import json

# Fetch Fear & Greed Index
with urllib.request.urlopen("https://api.alternative.me/fng/") as r:
    fng_data = json.loads(r.read())

# Fetch S&P 500
with urllib.request.urlopen("https://query2.finance.yahoo.com/v8/finance/chart/%5EGSPC?interval=1d&range=1d") as r:
    spx_data = json.loads(r.read())

# Fetch VIX
with urllib.request.urlopen("https://query2.finance.yahoo.com/v8/finance/chart/%5EVIX?interval=1d&range=1d") as r:
    vix_data = json.loads(r.read())

# Fetch ETFs
etfs = ["SPYM", "SCHG", "DYNF", "CGGR", "SPHQ", "XLG", "AIQ", "SOXQ", "PSI"]
etf_prices = {}
for etf in etfs:
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{etf}?interval=1d&range=1d"
    try:
        with urllib.request.urlopen(url) as r:
            d = json.loads(r.read())
            result = d["chart"]["result"][0]
            meta = result["meta"]
            price = meta.get("regularMarketPrice") or meta.get("previousClose")
            etf_prices[etf] = price
    except:
        etf_prices[etf] = "N/A"

print("=== FNG ===")
print(json.dumps(fng_data, indent=2))
print("\n=== SPX ===")
spx_meta = spx_data['chart']['result'][0]['meta']
print(f"Current: {spx_meta['regularMarketPrice']}")
print(f"Previous Close: {spx_meta['previousClose']}")
spx_change_pct = ((spx_meta['regularMarketPrice'] - spx_meta['previousClose']) / spx_meta['previousClose']) * 100
print(f"Change %: {spx_change_pct:.2f}%")

print("\n=== VIX ===")
vix_meta = vix_data['chart']['result'][0]['meta']
print(f"Current: {vix_meta['regularMarketPrice']}")
print(f"Previous Close: {vix_meta['previousClose']}")

print("\n=== ETFs ===")
for k, v in etf_prices.items():
    print(f"{k}: {v}")
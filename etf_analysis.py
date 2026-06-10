import urllib.request
import json

# Fetch Fear & Greed
fng_data = json.loads(urllib.request.urlopen("https://api.alternative.me/fng/").read())
fng = fng_data['data'][0]
fng_value = fng['value']
fng_class = fng['value_classification']

# Fetch S&P 500
sp500_raw = urllib.request.urlopen("https://query2.finance.yahoo.com/v8/finance/chart/%5EGSPC?interval=1d&range=1d").read()
sp500_data = json.loads(sp500_raw)
sp500_meta = sp500_data['chart']['result'][0]
sp500_cur = sp500_meta['meta']['regularMarketPrice']
sp500_prev = sp500_meta['meta']['previousClose']
sp500_chg = ((sp500_cur - sp500_prev) / sp500_prev) * 100

# Fetch VIX
vix_raw = urllib.request.urlopen("https://query2.finance.yahoo.com/v8/finance/chart/%5EVIX?interval=1d&range=1d").read()
vix_data = json.loads(vix_raw)
vix_cur = vix_data['chart']['result'][0]['meta']['regularMarketPrice']

# Fetch ETF prices
etfs = ['SPYM', 'SCHG', 'DYNF', 'CGGR', 'SPHQ', 'XLG', 'AIQ', 'SOXQ', 'PSI']
etf_prices = {}
for etf in etfs:
    try:
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{etf}?interval=1d&range=1d"
        raw = urllib.request.urlopen(url).read()
        data = json.loads(raw)
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        prev = data['chart']['result'][0]['meta']['previousClose']
        chg = ((price - prev) / prev) * 100
        etf_prices[etf] = {'price': price, 'chg': chg}
    except:
        etf_prices[etf] = {'price': 'ERR', 'chg': 0}

print(f"FNG: {fng_value} ({fng_class})")
print(f"SP500: {sp500_cur:.2f} ({sp500_chg:+.2f}%)")
print(f"VIX: {vix_cur:.2f}")
print(f"IS_RED_DAY: {sp500_chg < -1}")
print(f"IV_HIGH: {vix_cur > 40}")
print(f"FNG_LOW: {int(fng_value) < 25}")
print("ETFS:")
for etf, d in etf_prices.items():
    print(f"  {etf}: {d['price']} ({d['chg']:+.2f}%)")
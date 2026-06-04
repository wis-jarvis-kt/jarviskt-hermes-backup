import urllib.request
import json
import time

def fetch_url(url, retries=3, delay=2):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, timeout=10) as r:
                return json.loads(r.read())
        except Exception as e:
            if i < retries - 1:
                time.sleep(delay)
            else:
                raise e

def get_prev_close(data):
    """Get previous close from Yahoo chart data, handling None values."""
    closes = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    # Find the last non-None value for current price, second-to-last for prev close
    valid_closes = [c for c in closes if c is not None]
    if len(valid_closes) >= 2:
        return valid_closes[-2]  # previous close
    # Fallback to chartPreviousClose
    return data["chart"]["result"][0]["meta"]["chartPreviousClose"]

# Fetch Fear & Greed
print("Fetching Fear & Greed...")
fng_data = fetch_url("https://api.alternative.me/fng/")
fng = fng_data["data"][0]
fng_value = int(fng["value"])
fng_classification = fng["value_classification"]
print(f"FNG: {fng_value} ({fng_classification})")

time.sleep(1)

# Fetch S&P 500
print("Fetching S&P 500...")
spx_data = fetch_url("https://query2.finance.yahoo.com/v8/finance/chart/%5EGSPC?interval=1d&range=1d")
spx_meta = spx_data["chart"]["result"][0]["meta"]
spx_price = spx_meta["regularMarketPrice"]
spx_prev_close = get_prev_close(spx_data)
spx_change_pct = ((spx_price - spx_prev_close) / spx_prev_close) * 100
print(f"S&P 500: {spx_price:.2f} ({spx_change_pct:+.2f}%)")

time.sleep(1)

# Fetch VIX
print("Fetching VIX...")
vix_data = fetch_url("https://query2.finance.yahoo.com/v8/finance/chart/%5EVIX?interval=1d&range=1d")
vix_meta = vix_data["chart"]["result"][0]["meta"]
vix_price = vix_meta["regularMarketPrice"]
vix_prev_close = get_prev_close(vix_data)
vix_change_pct = ((vix_price - vix_prev_close) / vix_prev_close) * 100
print(f"VIX: {vix_price:.2f} ({vix_change_pct:+.2f}%)")

time.sleep(1)

# Fetch ETFs
etfs = ["SPYM", "SCHG", "DYNF", "CGGR", "SPHQ", "XLG", "AIQ", "SOXQ", "PSI"]
etf_prices = {}
for etf in etfs:
    print(f"Fetching {etf}...")
    try:
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{etf}?interval=1d&range=1d"
        d = fetch_url(url)
        meta = d["chart"]["result"][0]["meta"]
        price = meta["regularMarketPrice"]
        prev_close = get_prev_close(d)
        change_pct = ((price - prev_close) / prev_close) * 100
        etf_prices[etf] = {"price": price, "change_pct": change_pct}
        print(f"  {etf}: ${price:.2f} ({change_pct:+.2f}%)")
    except Exception as e:
        etf_prices[etf] = {"error": str(e)}
        print(f"  {etf}: ERROR - {e}")
    time.sleep(0.5)

# CSP Rules Evaluation
print("\n--- CSP ANALYSIS ---")
is_red_day = spx_change_pct < -1.0
iv_high = vix_price > 40
fear_low = fng_value < 25

print(f"Red Day (S&P down >1%): {is_red_day} ({spx_change_pct:.2f}%)")
print(f"IV > 40%: {iv_high} ({vix_price:.2f})")
print(f"Fear & Greed < 25: {fear_low} ({fng_value})")
put_day = is_red_day and iv_high and fear_low
print(f"PUT DAY: {put_day}")

# Build WhatsApp Report
print("\n\n=== WHATSAPP REPORT ===")
spx_color = "RED" if spx_change_pct < 0 else "GREEN"
print(f"S&P 500: {spx_price:.2f} {spx_color} ({spx_change_pct:+.2f}%)")
print(f"VIX: {vix_price:.2f} ({vix_change_pct:+.2f}%)")
print(f"Fear & Greed: {fng_value} - {fng_classification}")

if put_day:
    verdict = "PUT DAY - SELL CASH SECURED PUTS"
else:
    verdict = "NOT A PUT DAY"
print(f"\nTODAY'S VERDICT: {verdict}")

if not put_day:
    if spx_change_pct > 0.5:
        print("GREEN DAY: Consider covered CALL strategy")
    else:
        print("NEUTRAL: Wait for better entry")

print("\nETF Prices:")
for etf, data in etf_prices.items():
    if "error" not in data:
        ecolor = "+" if data['change_pct'] > 0 else "-"
        print(f"  {ecolor} {etf}: ${data['price']:.2f} ({data['change_pct']:+.2f}%)")
    else:
        print(f"  -- {etf}: ERROR")

print("\nCSP Entry Triggers (ALL must be met for PUT):")
print(f"  S&P down >1%: {'YES' if is_red_day else 'NO'} ({spx_change_pct:.2f}%)")
print(f"  IV >40%: {'YES' if iv_high else 'NO'} ({vix_price:.2f})")
print(f"  Fear & Greed <25: {'YES' if fear_low else 'NO'} ({fng_value})")
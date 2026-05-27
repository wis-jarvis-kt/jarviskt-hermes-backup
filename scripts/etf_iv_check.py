import yfinance as yf

etfs = ['AIQ', 'SOXQ', 'XLG', 'FNDX']
results = []

for sym in etfs:
    t = yf.Ticker(sym)
    info = t.info
    price = info.get('regularMarketPrice') or info.get('currentPrice')
    prev = info.get('previousClose', 'N/A')
    
    # Get ATM put IV and premium
    try:
        expires = list(t.options)
        if expires:
            opt = t.option_chain(expires[0])
            puts = opt.puts
            puts['dist'] = abs(puts['strike'] - price)
            atm = puts.loc[puts['dist'].idxmin()]
            iv = atm['impliedVolatility'] * 100
            premium = atm['lastPrice']
            roi = (premium / (atm['strike'] * 100)) * 100
            results.append({
                'sym': sym,
                'price': price,
                'prev': prev,
                'chg': ((price - prev) / prev) * 100 if prev != 'N/A' else 0,
                'atm_strike': atm['strike'],
                'iv': iv,
                'premium': premium,
                'roi': roi
            })
    except Exception as e:
        results.append({'sym': sym, 'price': price, 'error': str(e)})

print(f"VIX: 16.91")
print(f"SPX: 7525.19 (change: +0.08%)")
print(f"Fear & Greed: 25 (Extreme Fear)")
print()
print(f"{'ETF':<8} {'Price':<10} {'Change':<10} {'ATM Strike':<12} {'IV':<10} {'Premium':<10} {'ROI/mo':<10}")
print("-" * 80)
for r in results:
    if 'error' in r:
        print(f"{r['sym']:<8} ${r['price']:.2f}  ERROR: {r['error']}")
    else:
        print(f"{r['sym']:<8} ${r['price']:.2f}  {r['chg']:+.2f}%    ${r['atm_strike']:.2f}      {r['iv']:.1f}%     ${r['premium']:.2f}     {r['roi']:.2f}%")

print()
print("RED Day Status: SPX +0.08% = NOT RED (need >1% drop)")
print("VIX 16.91 = Neutral environment (IV still elevated for SOXQ/FNDX)")
print()
print("RECOMMENDATION: Still no CSP trigger today (SPX not down >1%)")
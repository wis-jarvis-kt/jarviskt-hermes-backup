import yfinance as yf

# Debug SOXQ specifically
sym = 'SOXQ'
t = yf.Ticker(sym)
info = t.info
price = info.get('regularMarketPrice') or info.get('currentPrice')
print(f"SOXQ price: {price}")

try:
    expires = list(t.options)
    print(f"Expiration dates: {expires[:5]}")
    
    if expires:
        opt = t.option_chain(expires[0])
        puts = opt.puts
        print(f"\nTotal puts: {len(puts)}")
        print(f"Puts columns: {puts.columns.tolist()}")
        
        # Show first few puts
        print(f"\nFirst 5 puts:")
        print(puts[['strike', 'lastPrice', 'bid', 'ask', 'impliedVolatility', 'volume']].head())
        
        # Find ATM
        puts['dist'] = abs(puts['strike'] - price)
        atm_idx = puts['dist'].idxmin()
        atm = puts.loc[atm_idx]
        print(f"\nATM Put:")
        print(f"  Strike: {atm['strike']}")
        print(f"  Last Price: {atm['lastPrice']}")
        print(f"  Bid: {atm['bid']}")
        print(f"  Ask: {atm['ask']}")
        print(f"  IV: {atm['impliedVolatility']}")
        print(f"  Volume: {atm['volume']}")
        print(f"  Distance from ATM: {atm['dist']}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
import yfinance as yf

sym = 'SOXQ'
t = yf.Ticker(sym)
info = t.info
price = info.get('regularMarketPrice') or info.get('currentPrice')

print(f"SOXQ price: ${price}")
print(f"Expires: {list(t.options)[:4]}")
print()

# Try next expiration
expires = list(t.options)
for exp_date in expires[:2]:
    print(f"=== Expiration: {exp_date} ===")
    opt = t.option_chain(exp_date)
    puts = opt.puts
    
    # Show all puts with IV
    for _, row in puts.iterrows():
        print(f"  Strike: ${row['strike']:.0f}  IV: {row['impliedVolatility']*100:.1f}%  Last: ${row['lastPrice']:.2f}  Vol: {row['volume']}")
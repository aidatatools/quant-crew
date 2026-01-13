import yfinance as yf

tickers = yf.Tickers('2330.TW TSM NVDA GOOG')

# access each ticker using (example)
#print(tickers.tickers['NVDA'].info)

print(tickers.tickers['2330.TW'].history(period="3mo"))

#print(tickers.tickers['TSM'].history(period="1mo"))

#print(tickers.tickers['GOOG'].actions)
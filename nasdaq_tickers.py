import yfinance as yf
fh = open('nasdaqlisted.txt')

tickers = []

for line in fh :
    end_ticker = line.find('|')
    tickers.append(line[0:end_ticker])


print("TKR", "LOW", "CRNT")

for ticker in tickers :
    try:
        stock = yf.Ticker(ticker)
        stock_low = stock.info['fiftyTwoWeekLow']
        stock_current = stock.info['regularMarketPreviousClose']
        if ((stock_current - stock_low) / stock_current) < .05 :
            print(ticker, stock_low, stock_current)
    except:
        continue


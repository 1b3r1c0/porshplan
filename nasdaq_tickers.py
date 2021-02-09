import yfinance as yf
fh = open('nasdaqlisted.txt')

tickers = []

for line in fh :
    end_ticker = line.find('|')
    tickers.append(line[0:end_ticker])




for ticker in tickers :
    try:
        stock = yf.Ticker(ticker)
        stock_low = stock.info['fiftyTwoWeekLow']
        stock_current = stock.info['regularMarketPreviousClose']
        #print(ticker,"-",stock_current,stock_low)
        if stock_low <= stock_current:
            percentBelow52WeekLow = 100 * (stock_current - stock_low) / stock_current
            # debug
            print(ticker,round(percentBelow52WeekLow, 1))
    except:
        print("wrong ticker")



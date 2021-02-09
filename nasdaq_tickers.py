import yfinance as yf
fh = open('nasdaqlisted.txt')

tickers = []

for line in fh :
    end_ticker = line.find('|')
    tickers.append(line[0:end_ticker])




for ticker in tickers :
    try:
        stock = yf.Ticker(ticker)
        stock_price = stock.info['regularMarketPreviousClose']
        print(ticker,"-",stock_price)
    except:
        print("wrong ticker")


    #try:
     #   print(stock_price)
    #except:
     #   print("nah")

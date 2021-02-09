import yfinance as yf

# Where did this file come from?
# todo: probably should add it ti this script as a function
fh = open('nasdaqlisted.txt')

# Initialize vars
tickers = []
lows = []
firstRun = True

# Create a list of stock tickers (symbols)
for line in fh :
    if firstRun :
        # Don't add anything from the header row of the CSV to this list
        firstRun = False
        continue
    else:
        # get the ticker symbol and add it to a list
        # example line from text file:
        # AACQ|Artius Acquisition Inc. - Class A Common Stock|S|N|N|100|N|N
        tickers.append(line.split('|')[0])
        # debug         print (tickers)        junk =input("paused")

# debug  print(len(tickers)) #junk =input("paused")

# todo: download the 52 week low and current price for each stock
# todo check if the data has already been downloaded for the current day
# todo use the day's stored data instead of re-downloading it each time the script is run

# Loop through each of the symbols
for ticker in tickers :
    # sometimes yfinance can't find a specific symbol
    try:
        # put the info for a symbol into an obj
        stock = yf.Ticker(ticker)
        
        # Get the stock's 52-week low
        stock52WeekLow = stock.info['fiftyTwoWeekLow']

        # Get the stock's current price
        stockCurrentPrice = stock.info['regularMarketPreviousClose']

        # check if the stock is within 5% of its 52 week low
        if ((stockCurrentPrice - stock52WeekLow) / stockCurrentPrice) <  .05:
            # Add the symbol to a list
            lows.append(ticker)
            # debug
            # print(
            #     "lows:",lows,
            #     ", ticker:",ticker,
            #     ", stock52WeekLow:",stock52WeekLow,
            #     ", stockCurrentPrice:",stockCurrentPrice
            # )
            # junk =input("paused")

    except:
        continue

# todo we should print out other useful info about the lows here
print("Found these lows that may be worth checking out")
for low in lows:
    print(low)

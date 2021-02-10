import yfinance as yf
from datetime import datetime
from pathlib import Path

# todo: add a function to this script for creating the nasdaqlisted.txt file
TEXT_FILE_WITH_TICKERS = 'nasdaqlisted.txt'
FILENAME_STOCK_INFO = "stock-info-"
FILENAME_STOCK_INFO_EXTENSION = ".csv"

# # Initialize vars
# tickers = []
# lows = []
#
def get_stock_tickers(ticker_file) :

    # example lines from text file:
    # Symbol|Security Name|Market Category|Test Issue|Financial Status|Round Lot Size|ETF|NextShares
    # AAON|AAON, Inc. - Common Stock|Q|N|N|100|N|N

    stock_tickers = []

    with open(ticker_file) as fh:
        nasdaq_stock_symbols = fh.readlines()

    first_run = True

    # Create a list of stock symbols
    for line in nasdaq_stock_symbols :
        if first_run :
            # Don't add anything from the header row of the CSV
            first_run = False
            continue
        else:
            # get the ticker symbol and add it to a list
            stock_tickers.append(line.split('|')[0])

    return(stock_tickers)

def create_file_name(name_before_date, file_extension) :
    # Create filename for the CSV to save stock info in
    # date is formated like this: 2020-12-05
    file_name = name_before_date + datetime.now().strftime("%Y-%m-%d") + file_extension

    # Check if the file already exists in the local folder
    if Path(file_name).is_file():
        return(file_name, True)
    else:
        return(file_name, False)

def get_stock_info(symbols, file_name) :
    list_of_dicts = []
    # Loop through each of the symbols
    for symbol in symbols:
        # yfinance blows up when it can't find a symbol
        try:
            # Retrieve info for a symbol and stick it in an obj
            stock = yf.Ticker(symbol)

            list_of_dicts.append(
                {
                    'symbol' : symbol,
                    'fiftyTwoWeekLow' : stock.info['fiftyTwoWeekLow'],
                    'regularMarketPreviousClose' : stock.info['regularMarketPreviousClose']
                }
            )
        except:
            continue


    # Create a line to save in the CSV
    # list_of_dicts = symbol + "," + stock52WeekLow + "," + stockCurrentPrice

# if __name__ == '__main__':

# Get a list of stock tickers to evaluate
tickers = get_stock_tickers(TEXT_FILE_WITH_TICKERS)
# print(tickers)

# Create a filename with date to save the stock info in
fileName, exists = create_file_name(FILENAME_STOCK_INFO, FILENAME_STOCK_INFO_EXTENSION)
# print(fileName, exists)

# Test if the file already exists
if exists :
    print("file exists do something")
    #     # Open a filehandle as "a"ppend

#     fhStockInfo = open(fileName, 'a')
else:
    get_stock_info(tickers, fileName)
    # print("file DOesn't exist do something else")
#     # Open a filehandle as "a"ppend
#     fhStockInfo = open(fileName, 'a')
#

#
# check if the stock is within 5% of its 52 week low
# if ((stockCurrentPrice - stock52WeekLow) / stockCurrentPrice) < .05:
    # Add the symbol to a list
#    lows.append(ticker)
    # debug
    # print(
    #     "lows:",lows,
    #     ", ticker:",ticker,
    #     ", stock52WeekLow:",stock52WeekLow,
    #     ", stockCurrentPrice:",stockCurrentPrice
    # )
    # junk =input("paused")

# todo we should print out other useful info about the lows here
#print("Found these lows that may be worth checking out")
#for low in lows:
#    print(low)

# todo: download the 52 week low and current price for each stock
# todo check if the data has already been downloaded for the current day
# todo use the day's stored data instead of re-downloading it each time the script is run

# Download stock data then export as CSV
# data_df = yf.download("AAPL", start="2020-02-01", end="2020-03-20")
# data_df.to_csv('aapl.csv')

# debug        print (tickers)        junk =input("paused")
# debug  print(len(tickers)) #junk =input("paused")
# debug        print("write: no exception") ; input("RTN to continue, CTL+c to stop")
# debug        print("open: no exception") ; input("RTN to continue, CTL+c to stop")
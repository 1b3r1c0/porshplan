import yfinance as yf
from datetime import datetime
from pathlib import Path

# todo specify this value as a script argument and use argparse
# Specify how close the current price should be to a stock's 52 week low
# For example, a value of .05 would mean within 5%
WITHIN = .01

# todo add a function to this script for creating the nasdaqlisted.txt file
# Specify the filename of the file containing stock tickers. Must be formatted like this:
# Symbol|Security Name|Market Category|Test Issue|Financial Status|Round Lot Size|ETF|NextShares
# AAON|AAON, Inc. - Common Stock|Q|N|N|100|N|N
TEXT_FILE_WITH_TICKERS = 'nasdaqlisted.txt'
# For debugging/testing use a file just a few entries
# TEXT_FILE_WITH_TICKERS = 'TEST.txt'

# Daily pulls of stock info are saved in this file in the same folder as this script
# Example filename: stock-info-2021-02-10.csv
FILENAME_STOCK_INFO = "stock-info-"

# Daily findings of stocks close to their 52-week lows are saved here
# Example filename: lows-2021-02-10.csv
FILENAME_LOWS = 'lows-'


def get_stock_tickers(ticker_file):
    # example lines from text file:
    # Symbol|Security Name|Market Category|Test Issue|Financial Status|Round Lot Size|ETF|NextShares
    # AAON|AAON, Inc. - Common Stock|Q|N|N|100|N|N

    stock_tickers = []

    with open(ticker_file) as fh:
        nasdaq_stock_symbols = fh.readlines()

    first_run = True

    # Create a list of stock symbols
    for line in nasdaq_stock_symbols:
        if first_run:
            # Don't add anything from the header row of the CSV
            first_run = False
            continue
        else:
            # get the ticker symbol and add it to a list
            stock_tickers.append(line.split('|')[0])

    return stock_tickers


def create_file_name(name_before_date, file_extension):
    # Create filename for the CSV to save stock info in
    # date is formatted like this: 2020-12-05
    file_name = name_before_date + datetime.now().strftime("%Y-%m-%d") + file_extension

    # Check if the file already exists in the local folder
    if Path(file_name).is_file():
        return file_name, True
    else:
        return file_name, False


def get_stock_info(symbols, file_name):
    # todo we should save other useful info about the potential low stocks here
    list_of_dicts = []
    # Loop through each of the symbols
    for symbol in symbols:
        # yfinance blows up when it can't find a symbol
        try:
            # Retrieve info for a symbol and stick it in an obj
            stock = yf.Ticker(symbol)

            list_of_dicts.append(
                {
                    'symbol': symbol,
                    'fiftyTwoWeekLow': stock.info['fiftyTwoWeekLow'],
                    'regularMarketPreviousClose': stock.info['regularMarketPreviousClose']
                }
            )
        except NameError:
            continue

    # Open a file handle as "a"ppend
    fh_stock_info = open(file_name, 'a')

    for dctnry in list_of_dicts:
        try:
            line = (dctnry['symbol']
                    + ","
                    + str(dctnry['fiftyTwoWeekLow'])
                    + ","
                    + str(dctnry['regularMarketPreviousClose'])
                    )
            fh_stock_info.write(line)
            fh_stock_info.write("\n")
        except NameError:
            continue

    fh_stock_info.close()


def get_lows(file_name_input, file_name_output):
    # Input: filename for CSV containing symbol,52wlow,current
    # output: CSV containing symbol,52wlow,current for symbols within 5% of their 52 week lows

    with open(file_name_input) as fh:
        lines = fh.readlines()

    # create a filename using the current date
    output_file_name_date = create_file_name(file_name_output, '.csv')

    # todo when lows already exists, delete it or overwrite it or something
    # Open a file handle as "a"ppend
    # output_file_name_date is a tuple with 2 elements
    fh_lows = open(output_file_name_date[0], 'a')

    for line in lines:
        data = line.rstrip().split(",")

        # symbol = data[0]
        ftwl = float(data[1])
        current = float(data[2])
        percentage = (current - ftwl) / ftwl
        # print("percentage current within 52 week low")
        # print(symbol, percentage)

        # check if the stock is within 5% of its 52 week low
        if percentage < WITHIN:
            # Add the line to a list
            fh_lows.write(line)

    fh_lows.close()


if __name__ == '__main__':

    # Get a list of stock tickers to evaluate
    tickers = get_stock_tickers(TEXT_FILE_WITH_TICKERS)

    # Create a filename with date to save the stock info in and whether or not the file exists
    fileNameStockData, exists = create_file_name(FILENAME_STOCK_INFO, '.csv')

    if exists:
        # Just get the lows when the data has already been downloaded
        get_lows(fileNameStockData, FILENAME_LOWS)
    else:
        # First download the data (takes a very long time)
        get_stock_info(tickers, fileNameStockData)
        # get the lows after the data has been downloaded
        get_lows(fileNameStockData, FILENAME_LOWS)

# Download stock data then export as CSV
# data_df = yf.download("AAPL", start="2020-02-01", end="2020-03-20")
# data_df.to_csv('aapl.csv')

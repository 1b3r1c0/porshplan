
fh = open('nasdaqlisted.txt')

tickers = []

for line in fh :
    end_ticker = line.find('|')
    tickers.append(line[0:end_ticker])
print(tickers)

fh = open('otherlisted.txt')



for line in fh :
    end_ticker = line.find('|')
    print(line[0:end_ticker])
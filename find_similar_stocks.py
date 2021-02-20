import json
import finnhub
import datetime
from stocks_list import curr_stocks, watchlist_stocks
from keys import finnhub_api_key
import os
import time

finnhub_client = finnhub.Client(api_key=finnhub_api_key)

def readFile(name):
    currentDate = datetime.date.today().strftime("%Y%m%d")
    outfileName = "Data/"+ currentDate + "/" + name + ".json"

    with open(outfileName, 'r') as outfile:
        data = json.load(outfile)
        return data

def createFile(data, name):

    outfileName = "Data/" + name + ".json"
    
    with open(outfileName, 'w') as outfile:
        json.dump(data,outfile)

def findSimilarStocks():
    
    similar_stocks = []

    for stock in curr_stocks:

        print(stock)

        tickers = finnhub_client.company_peers(stock)
        related_stocks = []
        for ticker in tickers:
            if (ticker == stock):
                continue
            else:
                related_stocks.append(ticker)

        for ticker in related_stocks[:4]:
            
            if (ticker in similar_stocks):
                continue
            elif (ticker in watchlist_stocks):
                continue
            elif (ticker in curr_stocks):
                continue
            elif ("." in ticker):
                continue
            else:
                similar_stocks.append(ticker)
        
    # time.sleep(30)

    for stock in watchlist_stocks:
        
        print(stock)

        tickers = finnhub_client.company_peers(stock)

        related_stocks = []
        for ticker in tickers:
            if (ticker == stock):
                continue
            else:
                related_stocks.append(ticker)
        


        for ticker in related_stocks[:4]:
            
            if (ticker in similar_stocks):
                continue
            elif (ticker in watchlist_stocks):
                continue
            elif (ticker in curr_stocks):
                continue
            elif ("." in ticker):
                continue
            else:
                similar_stocks.append(ticker)
    
    return similar_stocks

similar_stocks = findSimilarStocks()

createFile(similar_stocks, 'similar_stocks_list')





import finnhub
import datetime
import yahoo_earnings_calendar
import json
import time
from keys import finnhub_api_key

# Setup Imports
finnhub_client = finnhub.Client(api_key=finnhub_api_key)
yec = yahoo_earnings_calendar.YahooEarningsCalendar()

curr_stocks = ['ABNB','DIS','UBER','SNOW','EXPE','BABA','BA','DDOG','LUV','TGT','ALK','CVNA']

watchlist_stocks = ['XOM','JNJ','NFLX','PINS','PYPL','NVDA','V']

def createStockDetails(stocks):
    
    stockStatistics = []

    for stock in stocks:

        print(stock)

        stockDetails = {}
        priceTargets = {}
        stockStats = {}
        currentPrice = {}
        stockRecommendations = {}

        # Finnhub Price Target Data

        stockPriceTargets = finnhub_client.price_target(stock)

        pricetargetshigh = stockPriceTargets.get('targetHigh')
        pricetargetslow = stockPriceTargets.get('targetLow')
        pricetargetsmean = stockPriceTargets.get('targetMean')
        pricetargetsmedian = stockPriceTargets.get('targetMedian')

        priceTargets["HIGH"] = pricetargetshigh
        priceTargets["LOW"] = pricetargetslow
        priceTargets["MEAN"] = pricetargetsmean
        priceTargets["MEDIAN"] = pricetargetsmedian

        
        # Stock Prices for Today
        
        stockCurrentPrice = finnhub_client.quote(stock)

        closePrice = stockCurrentPrice.get('c')
        highPrice = stockCurrentPrice.get('h')
        lowPrice = stockCurrentPrice.get('l')
        openPrice = stockCurrentPrice.get('o')
        previousClose = stockCurrentPrice.get('pc')

        currentPrice["Open"] = openPrice
        currentPrice["Close"] = closePrice
        currentPrice["High"] = highPrice
        currentPrice["Low"] = lowPrice
        currentPrice["Previous Close"] = previousClose

        # Stock Information

        stockProfile = finnhub_client.company_profile2(symbol=stock)

        outstandingShares = stockProfile.get('shareOutstanding')
        marketCap = stockProfile.get('marketCapitalization')
        industry = stockProfile.get('finnhubIndustry')
        name = stockProfile.get('name')

         # Next Earning Date

        nextDateUnix = int(yec.get_next_earnings_date(stock))
        nextDateFormatted = datetime.datetime.utcfromtimestamp(nextDateUnix).strftime('%m-%d-%Y')

        stockStats['Name'] = name
        stockStats['Industry'] = industry
        stockStats['Market Cap'] = marketCap
        stockStats['Outstanding Shares'] = outstandingShares
        stockStats['Next Earnings Date'] = nextDateFormatted

        # Stock Recommendations

        stockRecs = finnhub_client.recommendation_trends(stock)

        stockRecommendations['Strong Buy'] = stockRecs[0].get('strongBuy')
        stockRecommendations['Buy'] = stockRecs[0].get('buy')
        stockRecommendations['Hold'] = stockRecs[0].get('hold')
        stockRecommendations['Sell'] = stockRecs[0].get('sell')
        stockRecommendations['Strong Sell'] = stockRecs[0].get('strongSell')
        stockRecommendations['Last Update'] = stockRecs[0].get('period')

        stockDetails['Ticker'] = stock
        stockDetails['Stock Information'] = stockStats
        stockDetails['Stock Pricing'] = currentPrice
        stockDetails['Stock Price Targets'] = priceTargets
        stockDetails['Stock Recommendations'] = stockRecommendations

        stockStatistics.append(stockDetails)
    return stockStatistics

def createFile(data, name):
    currentDate = datetime.date.today().strftime("%Y%m%d")
    outfileName = "Data/" + name + "_" + currentDate + ".json"
    
    with open(outfileName, 'w') as outfile:
        json.dump(data,outfile)

print("Getting Stock Data for Owned Stocks")

currStockDetails = createStockDetails(curr_stocks)
currStockDetailsFormatted = json.dumps(currStockDetails,indent=2)
createFile(currStockDetails, "owned_stocks")

print(currStockDetailsFormatted)

print("Sleeping for 60 seconds!")
time.sleep(60)
print("Sleep Ends!")

print("Getting Stock Data for Watch List Stocks")

watchlistStocksDetails = createStockDetails(watchlist_stocks)
watchlistStocksDetailsFormatted = json.dumps(watchlistStocksDetails, indent=2)
createFile(watchlistStocksDetails, "watchlist_stocks")

print(watchlistStocksDetailsFormatted)
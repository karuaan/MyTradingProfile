
import finnhub
import datetime
import yahoo_earnings_calendar
import json
import time
from keys import finnhub_api_key
import os

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
        stockAnalytics = {}

        # Finnhub Price Target Data

        stockPriceTargets = finnhub_client.price_target(stock)

        pricetargetshigh = stockPriceTargets.get('targetHigh')
        pricetargetslow = stockPriceTargets.get('targetLow')
        pricetargetsmean = stockPriceTargets.get('targetMean')
        pricetargetsmedian = stockPriceTargets.get('targetMedian')
        deviationInHighPrice = ((pricetargetshigh - pricetargetsmedian) / pricetargetsmedian) * 100
        deviationInLowPrice = ((pricetargetsmedian - pricetargetslow) / pricetargetsmedian) * 100

        priceTargets["HIGH"] = pricetargetshigh
        priceTargets["LOW"] = pricetargetslow
        priceTargets["MEAN"] = pricetargetsmean
        priceTargets["MEDIAN"] = pricetargetsmedian
        priceTargets["High Median Deviation"] = deviationInHighPrice
        priceTargets["High Low Deviation"] = deviationInLowPrice

        
        # Stock Prices for Today
        
        stockCurrentPrice = finnhub_client.quote(stock)

        closePrice = stockCurrentPrice.get('c')
        highPrice = stockCurrentPrice.get('h')
        lowPrice = stockCurrentPrice.get('l')
        openPrice = stockCurrentPrice.get('o')
        previousClose = stockCurrentPrice.get('pc')
        changeOpenToClose = ((closePrice - openPrice) / openPrice) * 100
        changeHighLow = ((highPrice - lowPrice) / lowPrice) * 100
        changeTodayYesterday = ((closePrice - previousClose) / 100) * 100

        currentPrice["Open"] = openPrice
        currentPrice["Close"] = closePrice
        currentPrice["High"] = highPrice
        currentPrice["Low"] = lowPrice
        currentPrice["Previous Close"] = previousClose
        currentPrice["Change Open to Close"] = changeOpenToClose
        currentPrice["Change High Low"] = changeHighLow
        currentPrice["Change Today Close Yesterday Close"] = changeTodayYesterday

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

        strongBuy = stockRecs[0].get('strongBuy')
        buys = stockRecs[0].get('buy')
        holds = stockRecs[0].get('hold')
        sell = stockRecs[0].get('sell')
        strongSells = stockRecs[0].get('sell')

        stockRecommendations['Strong Buy'] = stockRecs[0].get('strongBuy')
        stockRecommendations['Buy'] = stockRecs[0].get('buy')
        stockRecommendations['Hold'] = stockRecs[0].get('hold')
        stockRecommendations['Sell'] = stockRecs[0].get('sell')
        stockRecommendations['Strong Sell'] = stockRecs[0].get('strongSell')
        stockRecommendations['Last Update'] = stockRecs[0].get('period')

        # Related Stocks

        related_stocks_list = finnhub_client.company_peers(stock)

        # Stock Analysis

        currPriceMedian = ((closePrice - pricetargetsmedian) / pricetargetsmedian)
        currPriceLow = ((closePrice - pricetargetslow) / pricetargetslow)
        currPriceHigh = ((closePrice - pricetargetshigh) / pricetargetshigh)
        totalRecs = strongBuy + buys + holds + sell + strongSells
        buyRating = (((strongBuy * 2) +  buys) / totalRecs) * 100
        holdRating = (holds / totalRecs) * 100
        sellRating = (((strongSells * 2) + sell) / totalRecs) * 100

        stockAnalytics["Price to High Target Deviation"] = currPriceHigh
        stockAnalytics["Price to Median Target Deviation"] = currPriceMedian
        stockAnalytics["Price to Low Target Deviation"] = currPriceLow
        stockAnalytics["Buy Rating"] = buyRating
        stockAnalytics["Hold Rating"] = holdRating
        stockAnalytics["Sell Rating"] = sellRating

        stockDetails['Ticker'] = stock
        stockDetails['Stock Information'] = stockStats
        stockDetails['Stock Pricing'] = currentPrice
        stockDetails['Stock Analysis'] = stockAnalytics
        stockDetails['Stock Price Targets'] = priceTargets
        stockDetails['Stock Recommendations'] = stockRecommendations
        stockDetails['Related Stocks'] = related_stocks_list[1:]

        stockStatistics.append(stockDetails)
    return stockStatistics

def createFile(data, name):
    currentDate = datetime.date.today().strftime("%Y%m%d")
    outfileName = "Data/"+ currentDate + "/" + name + ".json"
    newDir = "Data/" +currentDate
    isDir = os.path.isdir(newDir)

    if (isDir == False):
        os.mkdir(newDir)
    
    with open(outfileName, 'w') as outfile:
        json.dump(data,outfile)

# def get_related_stocks(stocks):

#     related_stocks_list = []

#     for stock in stocks:

#         print(stock)

#         stock_related = {}

#         related_stocks_list = finnhub_client.company_peers(stock)

#         stock_related['Ticker'] = stock
#         stock_related['Related List'] = related_stocks_list

#         related_stocks_list.append(stock_related)

#     return related_stocks_list


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


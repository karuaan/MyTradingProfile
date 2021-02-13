
import finnhub
import datetime
import yahoo_earnings_calendar
import json
from keys import finnhub_api_key

# Setup Imports
finnhub_client = finnhub.Client(api_key=finnhub_api_key)
yec = yahoo_earnings_calendar.YahooEarningsCalendar()


stockStatistics = []

curr_stocks=['ABNB','DIS','UBER','SNOW','EXPE','BABA','BA','DDOG','LUV','TGT','ALK','CVNA']

def createStockDetails(stocks: list):
    
    stockStatistics = []

    for stock in curr_stocks:

        print(stock)

        stockDetails = {}
        priceTargets = {}
        stockStats = {}
        currentPrice = {}

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

        stockDetails['Ticker'] = stock
        stockDetails['Stock Information'] = stockStats
        stockDetails['Stock Pricing'] = currentPrice
        stockDetails['Stock Price Targets'] = priceTargets

        stockStatistics.append(stockDetails)

    return stockStatistics

stockDetails = createStockDetails(curr_stocks)

stockDetailsFormatted = json.dumps(stockDetails,indent=2)

currentDate = datetime.date.today().strftime("%Y%m%d")

outfileName = "Data/owned_stocks_data_" + currentDate + ".json"

with open(outfileName, 'w') as outfile:
    json.dump(stockDetails,outfile)

# print(airbnbNextEarningsUnix)
# print(airbnbNextEarningDate)
# print(quote)
print(stockDetailsFormatted)
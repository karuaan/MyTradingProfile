import finnhub
import datetime
import json
import time
from keys import finnhub_api_key
from stocks_list import curr_stocks, watchlist_stocks
import os

# Setup Imports
finnhub_client = finnhub.Client(api_key=finnhub_api_key)

def createFile(data, name):
    currentDate = datetime.date.today().strftime("%Y%m%d")
    outfileName = "Data/" + currentDate + "/" + name + ".json"
    newDir = "Data/" +currentDate
    isDir = os.path.isdir(newDir)

    if (isDir == False):
        os.mkdir(newDir)
    
    with open(outfileName, 'w') as outfile:
        json.dump(data,outfile)

def readFile(name):
    currentDate = datetime.date.today().strftime("%Y%m%d")
    outfileName = "Data/"+ name + ".json"

    with open(outfileName, 'r') as outfile:
        data = json.load(outfile)
        return data

def createStockDetails(stocks, name, name_analyst):
    
    stockStatistics = []

    yf_scraped_data = readFile(name)

    yf_analyst_scraped_data = readFile(name_analyst)

    count = 0

    for stock in stocks:

        print(stock)

        print(count)

        count += 1

        if (count > 10):
            time.sleep(60)
            count = 0

        for data in yf_scraped_data:

            name = data.get('Name')

            if (stock == name):
                yearlyHigh = float(data.get('Revelant Data').get('52 Week High'))
                yearlyLow = float(data.get('Revelant Data').get('52 Week Low'))
                peRatio = data.get('Revelant Data').get('PE Ratio')
                epsRatio = data.get('Revelant Data').get('EPS')
                earningsDateStart = data.get('Revelant Data').get('Next Earnings Date After')
                earningsDateEnd = data.get('Revelant Data').get('Next Earnings Date Before')
                yearlyEstimate = float(data.get('Revelant Data').get('1 Year EST'))

        for data in yf_analyst_scraped_data:
            name = data.get('Name')

            if (stock == name):

                # Analysis for Current Quarter EPS Data

                currentQuarterHighEstimatedEPS = float(data.get('Analysts Estimates Data')[0].get('Earnings Estimates Data')[2].get('High Estimate Data').get('Current Quarter'))
                currentQuarterAverageEstimatedEPS = float(data.get('Analysts Estimates Data')[0].get('Earnings Estimates Data')[0].get('Average Estimate Data').get('Current Quarter'))
                currentQuarterLowEstimatedEPS = float(data.get('Analysts Estimates Data')[0].get('Earnings Estimates Data')[1].get('Low Estimate Data').get('Current Quarter'))
                
                # Analysis for Current Quarter Revenue Data

                currentQuarterHighEstimatedRevenue = data.get('Analysts Estimates Data')[1].get('Revenue Estimates Data')[2].get('High Estimate Data').get('Current Quarter')
                currentQuarterAverageEstimatedRevenue = data.get('Analysts Estimates Data')[1].get('Revenue Estimates Data')[0].get('Average Estimate Data').get('Current Quarter')
                currentQuarterLowEstimatedRevenue = data.get('Analysts Estimates Data')[1].get('Revenue Estimates Data')[1].get('Low Estimate Data').get('Current Quarter')

                # Analysis for Current Quarter EPS Trend

                currentQuarterCurrentEstimatedEPS = float(data.get('Analysts Estimates Data')[2].get('EPS Trends Data')[0].get('Current Estimate Data').get('Current Quarter'))
                currentQuarter7DaysAgoEstimatedEPS = float(data.get('Analysts Estimates Data')[2].get('EPS Trends Data')[1].get('7 Days Ago Estimate Data').get('Current Quarter'))
                currentQuarter30DaysAgoEstimatedEPS = float(data.get('Analysts Estimates Data')[2].get('EPS Trends Data')[2].get('30 Days Ago Estimate Data').get('Current Quarter'))

                # Analysis for Next Quarter EPS Data

                nextQuarterHighEstimatedEPS = float(data.get('Analysts Estimates Data')[0].get('Earnings Estimates Data')[2].get('High Estimate Data').get('Next Quarter'))
                nextQuarterAverageEstimatedEPS = float(data.get('Analysts Estimates Data')[0].get('Earnings Estimates Data')[0].get('Average Estimate Data').get('Next Quarter'))
                nextQuarterLowEstimatedEPS = float(data.get('Analysts Estimates Data')[0].get('Earnings Estimates Data')[1].get('Low Estimate Data').get('Next Quarter'))
                
                # Analysis for Next Quarter Revenue Data

                nextQuarterHighEstimatedRevenue = data.get('Analysts Estimates Data')[1].get('Revenue Estimates Data')[2].get('High Estimate Data').get('Next Quarter')
                nextQuarterAverageEstimatedRevenue = data.get('Analysts Estimates Data')[1].get('Revenue Estimates Data')[0].get('Average Estimate Data').get('Next Quarter')
                nextQuarterLowEstimatedRevenue = data.get('Analysts Estimates Data')[1].get('Revenue Estimates Data')[1].get('Low Estimate Data').get('Next Quarter')

                # Analysis for Next Quarter EPS Trend

                nextQuarterCurrentEstimatedEPS = float(data.get('Analysts Estimates Data')[2].get('EPS Trends Data')[0].get('Current Estimate Data').get('Next Quarter'))
                nextQuarter7DaysAgoEstimatedEPS = float(data.get('Analysts Estimates Data')[2].get('EPS Trends Data')[1].get('7 Days Ago Estimate Data').get('Next Quarter'))
                nextQuarter30DaysAgoEstimatedEPS = float(data.get('Analysts Estimates Data')[2].get('EPS Trends Data')[2].get('30 Days Ago Estimate Data').get('Next Quarter'))

                # Analysis for Current Year EPS Data

                currentYearHighEstimatedEPS = float(data.get('Analysts Estimates Data')[0].get('Earnings Estimates Data')[2].get('High Estimate Data').get('Current Year'))
                currentYearAverageEstimatedEPS = float(data.get('Analysts Estimates Data')[0].get('Earnings Estimates Data')[0].get('Average Estimate Data').get('Current Year'))
                currentYearLowEstimatedEPS = float(data.get('Analysts Estimates Data')[0].get('Earnings Estimates Data')[1].get('Low Estimate Data').get('Current Year'))
                
                # Analysis for Next Quarter Revenue Data

                currentYearHighEstimatedRevenue = data.get('Analysts Estimates Data')[1].get('Revenue Estimates Data')[2].get('High Estimate Data').get('Current Year')
                currentYearAverageEstimatedRevenue = data.get('Analysts Estimates Data')[1].get('Revenue Estimates Data')[0].get('Average Estimate Data').get('Current Year')
                currentYearLowEstimatedRevenue = data.get('Analysts Estimates Data')[1].get('Revenue Estimates Data')[1].get('Low Estimate Data').get('Current Year')

                # Analysis for Next Quarter EPS Trend

                currentYearCurrentEstimatedEPS = float(data.get('Analysts Estimates Data')[2].get('EPS Trends Data')[0].get('Current Estimate Data').get('Current Year'))
                currentYear7DaysAgoEstimatedEPS = float(data.get('Analysts Estimates Data')[2].get('EPS Trends Data')[1].get('7 Days Ago Estimate Data').get('Current Year'))
                currentYear30DaysAgoEstimatedEPS = float(data.get('Analysts Estimates Data')[2].get('EPS Trends Data')[2].get('30 Days Ago Estimate Data').get('Current Year'))


        stockDetails = {}
        stockStats = {}
        currentPrice = {}
        stockRecommendations = {}
        stockAnalytics = {}
        analystEstimatedTrendsCurrentQuarter = {}
        analystEstimatedTrendsCurrentYear = {}


        # Analysts Trends Current Quarter

        analystEstimatedTrendsCurrentQuarter['High EPS'] = currentQuarterHighEstimatedEPS
        analystEstimatedTrendsCurrentQuarter['Average EPS'] = currentQuarterAverageEstimatedEPS
        analystEstimatedTrendsCurrentQuarter['Low EPS'] = currentQuarterLowEstimatedEPS
        analystEstimatedTrendsCurrentQuarter['High Revenue'] = currentQuarterHighEstimatedRevenue
        analystEstimatedTrendsCurrentQuarter['Low Revenue'] = currentQuarterLowEstimatedRevenue
        analystEstimatedTrendsCurrentQuarter['Current Estimated EPS'] = currentQuarterCurrentEstimatedEPS

        # Analysts Trends Current Year

        analystEstimatedTrendsCurrentYear['High EPS'] = currentYearHighEstimatedEPS
        analystEstimatedTrendsCurrentYear['Average EPS'] = currentYearAverageEstimatedEPS
        analystEstimatedTrendsCurrentYear['Low EPS'] = currentYearLowEstimatedEPS
        analystEstimatedTrendsCurrentYear['High Revenue'] = currentYearHighEstimatedRevenue
        analystEstimatedTrendsCurrentYear['Low Revenue'] = currentYearLowEstimatedRevenue
        analystEstimatedTrendsCurrentYear['Current Estimated EPS'] = currentYearCurrentEstimatedEPS

        # Stock Prices for Today
        
        stockCurrentPrice = finnhub_client.quote(stock)

        closePrice = stockCurrentPrice.get('c')
        highPrice = stockCurrentPrice.get('h')
        lowPrice = stockCurrentPrice.get('l')
        openPrice = stockCurrentPrice.get('o')
        previousClose = stockCurrentPrice.get('pc')
        changeOpenToClose = round(((closePrice - openPrice) / openPrice) * 100,2)
        changeHighLow = round(((highPrice - lowPrice) / lowPrice) * 100,2)
        changeTodayYesterday = round(((closePrice - previousClose) / previousClose) * 100,2)

        currentPrice["Open"] = openPrice
        currentPrice["Close"] = closePrice
        currentPrice["High"] = highPrice
        currentPrice["Low"] = lowPrice
        currentPrice["Previous Close"] = previousClose
        currentPrice["Change Open to Close"] = changeOpenToClose
        currentPrice["Daily Change"] = changeHighLow
        currentPrice["Change Today Close Yesterday Close"] = changeTodayYesterday

        # Stock Information

        stockProfile = finnhub_client.company_profile2(symbol=stock)

        outstandingShares = stockProfile.get('shareOutstanding')
        marketCap = stockProfile.get('marketCapitalization')
        industry = stockProfile.get('finnhubIndustry')
        name = stockProfile.get('name')

         # Next Earning Date

        stockStats['Name'] = name
        stockStats['Industry'] = industry
        stockStats['Market Cap'] = marketCap * 1000000
        stockStats['Outstanding Shares'] = outstandingShares * 1000000
        stockStats['Next Earnings Date After'] = earningsDateStart
        stockStats['Next Earnings Date Before'] = earningsDateEnd
        stockStats['PE Ratio'] = peRatio
        stockStats['EPS'] = epsRatio
        stockStats['1 Year EST'] = yearlyEstimate


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

        totalRecs = strongBuy + buys + holds + sell + strongSells
        buyRating = round((((strongBuy * 2) +  buys) / totalRecs) * 100,2)
        holdRating = round((holds / totalRecs) * 100,2)
        sellRating = round((((strongSells * 2) + sell) / totalRecs) * 100,2)
        yearlyDiff = yearlyHigh - yearlyLow
        yearlyDiffPercent = round(((yearlyHigh - yearlyLow) / yearlyLow) * 100,2)
        yealyEstDiff = round(yearlyEstimate - closePrice,2)
        yealyEstDiffPercent = round(((yearlyEstimate - closePrice) / closePrice) * 100,2)
        highEstimatedCurrentYearPE = round(closePrice / currentYearHighEstimatedEPS,2)
        lowEstimatedCurrentYearPE = round(closePrice / currentYearLowEstimatedEPS, 2)
        currentYearEatimatedPEChange = round(highEstimatedCurrentYearPE - lowEstimatedCurrentYearPE, 2)
        currentYearEatimatedPEChangePercent = abs(round(((highEstimatedCurrentYearPE - lowEstimatedCurrentYearPE) / lowEstimatedCurrentYearPE ) * 100,2))

        related_stocks_list = finnhub_client.company_peers(stock)

        related_stock_tickers = []

        for related_stock in related_stocks_list:
            if (related_stock == stock):
                continue
            else:
                related_stock_tickers.append(related_stock)
        
        related_stocks = []

        for tick in related_stock_tickers[:4]:

            if ("." in tick):
                continue
            else:
                related_stocks.append(tick)

        print(related_stocks)
        stockAnalytics["Buy Rating"] = buyRating
        stockAnalytics["Hold Rating"] = holdRating
        stockAnalytics["Sell Rating"] = sellRating
        stockAnalytics["52 Week Price Change"] = yearlyDiff
        stockAnalytics["52 Week Percent Increase"] = yearlyDiffPercent
        stockAnalytics["1 Year EST Deviation"] = yealyEstDiff
        stockAnalytics["1 Year EST Deviation Percentage"] = yealyEstDiffPercent
        stockAnalytics["Estimated High Yearly PE"] = highEstimatedCurrentYearPE
        stockAnalytics["Estimated Low Yearly PE"] = lowEstimatedCurrentYearPE
        stockAnalytics["Difference in Estimated Yearly PE"] = currentYearEatimatedPEChange
        stockAnalytics["Estimated Yearly PE Change Percent"] = currentYearEatimatedPEChangePercent

        stockDetails['Ticker'] = stock
        stockDetails['Stock Information'] = stockStats
        stockDetails['Stock Pricing'] = currentPrice
        stockDetails['Stock Analysis'] = stockAnalytics
        stockDetails['Stock Recommendations'] = stockRecommendations
        stockDetails['Current Quarter Analysts Estimates'] = analystEstimatedTrendsCurrentQuarter
        stockDetails['Current Year Analysts Estimates'] = analystEstimatedTrendsCurrentYear
        stockDetails['Related Stocks'] = related_stocks

        stockStatistics.append(stockDetails)
    return stockStatistics

print("Getting Stock Data for Owned Stocks")

currStockDetails = createStockDetails(curr_stocks, 'yf_owned_stocks', 'yf_owned_stocks_analyst_data')
currStockDetailsFormatted = json.dumps(currStockDetails,indent=2)
createFile(currStockDetails, "owned_stocks")

print("Sleeping for 60 seconds!")
time.sleep(60)
print("Sleep Ends!")

print("Getting Stock Data for Watch List Stocks!")

watchlistStocksDetails = createStockDetails(watchlist_stocks, 'yf_watchlist_stocks', 'yf_watchlist_stocks_analyst_data')
watchlistStocksDetailsFormatted = json.dumps(watchlistStocksDetails, indent=2)
createFile(watchlistStocksDetails, "watchlist_stocks")

print("Sleeping for 60 seconds!")
time.sleep(60)
print("Sleep Ends!")

print("Getting Stock Data for Similar Stocks!")

similar_stocks = readFile('similar_stocks_list')
watchlistStocksDetails = createStockDetails(similar_stocks, 'yf_similar_stocks', 'yf_similar_stocks_analyst_data')
watchlistStocksDetailsFormatted = json.dumps(watchlistStocksDetails, indent=2)
createFile(watchlistStocksDetails, "similar_stocks")
import requests
import finnhub
from pprint import pprint
from bs4 import BeautifulSoup
import os
import datetime
from datetime import timedelta
import prettify
from stocks_list import curr_stocks, watchlist_stocks
from keys import finnhub_api_key
import json

finnhub_client = finnhub.Client(api_key=finnhub_api_key)

def yf_stocks_analyst_data(stocks):
    
    stock_data = []

    for stock in stocks:

        data_dict = {}
        print(stock)
        # Make URL for Yahoo Finance
    
        URL = 'https://finance.yahoo.com/quote/{0}/analysis?p={0}'.format(stock)
        analysis_page = requests.get(URL)
        soup = BeautifulSoup(analysis_page.content, 'html.parser')

        dataTables = soup.find(id="Col1-0-AnalystLeafPage-Proxy")
        tablesList = dataTables.find_all('table')

        # Find all the Tables

        earningsEstimateTable  = tablesList[0]
        revenueEstimateTable = tablesList[1]
        epsTrendTable = tablesList[3]

        # Find all Data Rows of the Tables

        earningsEstimateDataRows = earningsEstimateTable.find_all('td')
        revenueEstimateDataRows = revenueEstimateTable.find_all('td')
        epsTrendDataRows = epsTrendTable.find_all('td')

        mainList = []

        # Earnings Estimates Table Parse

        earningsEstimateTableDict = {}
        earningsEstimatesTableList = []

        earningsEstimateTableDict['Table Name'] = "Earnings Estimate" 

        for index, data in enumerate(earningsEstimateDataRows):
            rowDict = {}
            indexDict = {}

            name = data.get_text()

            if (name == "Avg. Estimate"):

                indexDict['Current Quarter'] = earningsEstimateDataRows[index+1].get_text()
                indexDict['Next Quarter'] = earningsEstimateDataRows[index+2].get_text()
                indexDict['Current Year'] = earningsEstimateDataRows[index+3].get_text()

                rowDict['Name'] = name
                rowDict['Average Estimate Data'] = indexDict
                earningsEstimatesTableList.append(rowDict)

            elif (name == "Low Estimate"):

                indexDict['Current Quarter'] = earningsEstimateDataRows[index+1].get_text()
                indexDict['Next Quarter'] = earningsEstimateDataRows[index+2].get_text()
                indexDict['Current Year'] = earningsEstimateDataRows[index+3].get_text()

                rowDict['Name'] = name
                rowDict['Low Estimate Data'] = indexDict
                earningsEstimatesTableList.append(rowDict)

            elif (name == "High Estimate"):

                indexDict['Current Quarter'] = earningsEstimateDataRows[index+1].get_text()
                indexDict['Next Quarter'] = earningsEstimateDataRows[index+2].get_text()
                indexDict['Current Year'] = earningsEstimateDataRows[index+3].get_text()

                rowDict['Name'] = name
                rowDict['High Estimate Data'] = indexDict
                earningsEstimatesTableList.append(rowDict)

        earningsEstimateTableDict['Earnings Estimates Data'] = earningsEstimatesTableList

        mainList.append(earningsEstimateTableDict)

        # Revenue Estimates Table Parse

        revenueEstimateTableDict = {}
        revenueEstimatesTableList = []

        for index, data in enumerate(revenueEstimateDataRows):
            rowDict = {}
            indexDict = {}

            name = data.get_text()

            if (name == "Avg. Estimate"):

                indexDict['Current Quarter'] = revenueEstimateDataRows[index+1].get_text()
                indexDict['Next Quarter'] = revenueEstimateDataRows[index+2].get_text()
                indexDict['Current Year'] = revenueEstimateDataRows[index+3].get_text()

                rowDict['Name'] = name
                rowDict['Average Estimate Data'] = indexDict
                revenueEstimatesTableList.append(rowDict)

            elif (name == "Low Estimate"):

                indexDict['Current Quarter'] = revenueEstimateDataRows[index+1].get_text()
                indexDict['Next Quarter'] = revenueEstimateDataRows[index+2].get_text()
                indexDict['Current Year'] = revenueEstimateDataRows[index+3].get_text()

                rowDict['Name'] = name
                rowDict['Low Estimate Data'] = indexDict
                revenueEstimatesTableList.append(rowDict)

            elif (name == "High Estimate"):

                indexDict['Current Quarter'] = revenueEstimateDataRows[index+1].get_text()
                indexDict['Next Quarter'] = revenueEstimateDataRows[index+2].get_text()
                indexDict['Current Year'] = revenueEstimateDataRows[index+3].get_text()

                rowDict['Name'] = name
                rowDict['High Estimate Data'] = indexDict
                revenueEstimatesTableList.append(rowDict)

        revenueEstimateTableDict['Revenue Estimates Data'] = revenueEstimatesTableList

        mainList.append(revenueEstimateTableDict)

        # EPS Trends Table Parse

        epsTrendsTableDict = {}
        epsTrandsTableList = []

        for index, data in enumerate(epsTrendDataRows):
            rowDict = {}
            indexDict = {}

            name = data.get_text()

            if (name == "Current Estimate"):

                indexDict['Current Quarter'] = epsTrendDataRows[index+1].get_text()
                indexDict['Next Quarter'] = epsTrendDataRows[index+2].get_text()
                indexDict['Current Year'] = epsTrendDataRows[index+3].get_text()

                rowDict['Name'] = name
                rowDict['Current Estimate Data'] = indexDict
                epsTrandsTableList.append(rowDict)

            elif (name == "7 Days Ago"):

                indexDict['Current Quarter'] = epsTrendDataRows[index+1].get_text()
                indexDict['Next Quarter'] = epsTrendDataRows[index+2].get_text()
                indexDict['Current Year'] = epsTrendDataRows[index+3].get_text()

                rowDict['Name'] = name
                rowDict['7 Days Ago Estimate Data'] = indexDict
                epsTrandsTableList.append(rowDict)

            elif (name == "30 Days Ago"):

                indexDict['Current Quarter'] = epsTrendDataRows[index+1].get_text()
                indexDict['Next Quarter'] = epsTrendDataRows[index+2].get_text()
                indexDict['Current Year'] = epsTrendDataRows[index+3].get_text()

                rowDict['Name'] = name
                rowDict['30 Days Ago Estimate Data'] = indexDict
                epsTrandsTableList.append(rowDict) 

        epsTrendsTableDict['EPS Trends Data'] = epsTrandsTableList

        mainList.append(epsTrendsTableDict)

        data_dict['Name'] = stock
        data_dict['Analysts Estimates Data'] = mainList
        stock_data.append(data_dict)
    
    return stock_data

def createFile(data, name):

    outfileName = "Data/" + name + ".json"
    
    with open(outfileName, 'w') as outfile:
        json.dump(data,outfile)

owned_stocks_analyst_data = yf_stocks_analyst_data(curr_stocks)

createFile(owned_stocks_analyst_data, 'yf_owned_stocks_analyst_data')

watchlist_stocks_analyst_data = yf_stocks_analyst_data(watchlist_stocks)

createFile(watchlist_stocks_analyst_data, 'yf_watchlist_stocks_analyst_data')

similar_stocks_owned = findSimilarStocksOwned(curr_stocks)

similar_stocks_watchlist = findSimilarStocksWatchlist(watchlist_stocks)





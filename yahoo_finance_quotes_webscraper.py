import requests
from pprint import pprint
from bs4 import BeautifulSoup
import os
import datetime
import prettify
from stocks_list import curr_stocks, watchlist_stocks
import json

def yf_stocks_data(stocks):
   
   stock_data = []

   for stock in stocks:

       print(stock)

       URL = 'https://finance.yahoo.com/quote/{0}?p={0}'.format(stock)
       quote_page = requests.get(URL)

       soup = BeautifulSoup(quote_page.content, 'html.parser')
       quote_summary = soup.find(id='quote-summary')
       summary_elems = quote_summary.find_all('td')
       
       values_dict = {}
       main_dict = {}
       data_dict = {}

       for index, data in enumerate(summary_elems):
           if (data.get_text() == "52 Week Range"):
               values_dict["52 Week Range"] = index+1
           elif (data.get_text() == "PE Ratio (TTM)"):
               values_dict["PE Ratio"] = index+1
           elif (data.get_text() == "EPS (TTM)"):
               values_dict["EPS"] = index+1
           elif (data.get_text() == "1y Target Est"):
               values_dict["1 Year EST"] = index+1

       for key in values_dict:
           index = values_dict[key] 

           if (key == "52 Week Range"):
               yearlyRange = summary_elems[index].get_text()
               yearlyRangesplit = yearlyRange.split(" ")
               main_dict['52 Week Low'] = yearlyRangesplit[0]
               main_dict['52 Week High'] = yearlyRangesplit[2]
           else:
               main_dict[key] = summary_elems[index].get_text()
            
       data_dict['Name'] = stock
       data_dict['Revelant Data'] = main_dict
       stock_data.append(data_dict)
   return stock_data

def createFile(data, name):

    outfileName = "Data/" + name + ".json"
    
    with open(outfileName, 'w') as outfile:
        json.dump(data,outfile)

owned_data = yf_stocks_data(curr_stocks)
createFile(owned_data, 'yf_owned_stocks')

watch_list_data = yf_stocks_data(watchlist_stocks)
createFile(watch_list_data, 'yf_watchlist_stocks')

similar_stocks_data = yf_stocks_data(similar_stocks)
createFile(similar_stocks_data, 'yf_similar_stocks')



import requests
from pprint import pprint
from bs4 import BeautifulSoup
import os
import datetime
import prettify
from stocks_list import indexes
import json

def yf_index_data(indexList):
   
   index_data = []

   for index in indexList:
       print(index)

       index_dict = {}
       index_analytics = {}
       main_dict = {}

       URL = 'https://finance.yahoo.com/quote/%5E{0}?p=%5E{0}'.format(index)
       quote_page = requests.get(URL)

       soup = BeautifulSoup(quote_page.content, 'html.parser')
       quote_summary = soup.find(id='quote-summary')
       summary_elems = quote_summary.find_all('td')

       for count,elem in enumerate(summary_elems):
           
           name = elem.get_text()

           if (name == "Previous Close"):
               index_prev_close = float(summary_elems[count+1].get_text().replace(",",""))
               index_dict["Previous Close"] = summary_elems[count+1].get_text()

           elif (name == "Open"):
               index_open = float(summary_elems[count+1].get_text().replace(",",""))
               index_dict["Open"] = summary_elems[count+1].get_text()

               index_analytics["Prev Close to Open Change"] =  index_open - index_prev_close
               index_analytics["Prev Close to Open Change Percent"] =  round((index_open - index_prev_close) / index_prev_close * 100,2)

           elif (name == "Day's Range"):
               
               days_range = summary_elems[count+1].get_text()
               day_range_split = days_range.split(" ")
               day_low = float(day_range_split[0].replace(",",""))
               day_high = float(day_range_split[2].replace(",",""))
               day_diff = day_high - day_low
               day_diff_Percent = round(day_diff / day_low * 100, 2)
               
               index_dict["Day High"] = day_high
               index_dict["Day Low"] = day_low
               index_analytics["Daily Change"] = day_diff
               index_analytics["Daily Change Percent"] = day_diff_Percent

           elif (name == "52 Week Range"):

               yearlyRange = summary_elems[count+1].get_text()
               yearlyRangesplit = yearlyRange.split(" ")
               yealyLow  = float(yearlyRangesplit[0].replace(',',''))
               yearlyHigh = float(yearlyRangesplit[2].replace(',',''))
               yearly_diff = yearlyHigh - yealyLow
               yearly_diff_Percent = round((yearly_diff / yealyLow) * 100, 2)


               index_dict["52 Week High"] = day_high
               index_dict["52 Week Low"] = day_low
               index_analytics["52 Week Change"] = yearly_diff
               index_analytics["52 Week Change Percent"] = yearly_diff_Percent

       main_dict['Name'] = index
       main_dict['Index Data'] = index_dict
       main_dict['Index Analytics'] = index_analytics
           
       index_data.append(main_dict)
   return index_data

def createFile(data, name):
    currentDate = datetime.date.today().strftime("%Y%m%d")
    outfileName = "Data/" + currentDate + "/" + name + ".json"
    newDir = "Data/" +currentDate
    isDir = os.path.isdir(newDir)

    if (isDir == False):
        os.mkdir(newDir)
    
    with open(outfileName, 'w') as outfile:
        json.dump(data,outfile)


index_data = yf_index_data(indexes)

createFile(index_data, 'index_data')




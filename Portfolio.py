
import finnhub
import datetime
import yahoo_earnings_calendar
import pandas
from keys import finnhub_api_key

# Setup Imports
finnhub_client = finnhub.Client(api_key=finnhub_api_key)
yec = yahoo_earnings_calendar.YahooEarningsCalendar()

res = finnhub_client.quote('ABNB')

airbnbNextEarningsUnix = int(yec.get_next_earnings_date('ABNB'))

airbnbNextEarningDate = datetime.datetime.utcfromtimestamp(airbnbNextEarningsUnix).strftime('%m-%d-%Y')

print(res)
print(airbnbNextEarningsUnix)
print(airbnbNextEarningDate)
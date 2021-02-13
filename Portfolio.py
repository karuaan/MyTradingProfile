import finnhub
import datetime
from yahoo_earnings_calendar import YahooEarningsCalendar
from Keys.py import finnhub_api_key as fh_key

finnhub_client = finnhub.Client(api_key="fh_key")
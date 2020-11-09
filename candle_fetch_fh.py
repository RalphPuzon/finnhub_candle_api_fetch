#finnhub candle fetch

"""
Fetch stock candle data using Finnhub's API
"""
#main data fetch function:
"""
Function arguments:

	symbol  = ticker symbol for desired company goes here
	
	resolution = granularity of the data:
	
		1 (minute)
		
		5 (minutes)
		
		15 (minutes)
		
		30 (minutes)
		
		60 (minutes) 
		
		D(ay)
		
		W(eek) 
		
		M(onth)
		
	date_from = starting date, in american format with slashes (e.g. 01/13/2018)
	
	date_to = ending date, in american format with slashes (e.g. 01/13/2018)
	
	token = '*insert your finnhub api key here*'

Function returns:

	a pandas DataFrame.

columns:

	o - List of open prices for returned candles.
	
	h - List of high prices for returned candles.
	
	l - List of low prices for returned candles.
	
	c - List of close prices for returned candles.
	
	v - List of volume data for returned candles.
	
	t - List of timestamp for returned candles.
	
	s - Status of the response. This field can either be ok or no_data.
	
	
The function takes in the function arguments,  and formats the request URL to obtain the appropriate raw data. the
timestamp data is then further processed to obtain a readable date stamp, as well as a week index. The resulting table
is the function's returned output.
"""
def fetch_data(symbol, resolution, date_from, date_to):
   
	#imports:
	from configparser import ConfigParser as cfg
	import requests
	import pandas as pd
	import time
	import datetime

	#api token:
	cfg = cfg()
	cfg.read('./config.ini')
	token = cfg['token']['token']

	#remove futurewarning alert:
	import warnings
	warnings.simplefilter(action='ignore', category=FutureWarning)

	# converting dates to unix time:
	unix_from = time.mktime(datetime.datetime.strptime(date_from, "%m/%d/%Y").timetuple())
	unix_to = time.mktime(datetime.datetime.strptime(date_to, "%m/%d/%Y").timetuple())

	# format the get URL query:
	curr_req = (f"https://finnhub.io/api/v1/stock/candle?" 
				f"symbol={symbol}" 
				f"&resolution={resolution}" 
				f"&from={unix_from}" 
				f"&to={unix_to}" 
				f"&token={token}")
  
	df = pd.DataFrame(requests.get(curr_req).json())

	# format column names:
	df.columns = ['close', 'high', 'low', 'open', 'request_status',
				  'timestamp', 'volume']

	# add a readable date column:
	df['date'] = pd.to_datetime(df['timestamp'], unit='s')

	# add week counter:
	df['week'] = df['date'].dt.week

	return df

#TEST:
data_by_week = fetch_data('AAPL', 'W', '01/01/2018', '12/31/2018')
#testing the function:
print(data_by_week.head())

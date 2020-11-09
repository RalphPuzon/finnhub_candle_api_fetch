import os
os.chdir('E:\\ProjectDataFolder\\finnhub_candle_api_fetch')

#graph example
#import function:
from candle_fetch_fh import fetch_data
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

#fetch data:
data_by_week = fetch_data('AAPL', # ipo company symbol
							 'W', # granularity, here it's week
	  				'01/01/2018', # start date in US date format
	  				'12/31/2018') # end date in US date format

#EXAMPLE ANALYTICS:
#Ex. 1:
"""Plot the data of the stock closing price, highlighting the
52 week high and 52 week low."""

# fetch lowest price week:
lowest_price = min(data_by_week['close'])
lowest_week = data_by_week.loc[data_by_week['close'] == lowest_price]['week'].values[0]

# fetch highest price week:
highest_price = max(data_by_week['close'])
highest_week = data_by_week.loc[data_by_week['close'] == highest_price]['week'].values[0]

# main graph of closing prices:
fig = plt.figure()
plt.plot(data_by_week['week'], data_by_week['close'], color='green')
plt.xlim(1,None)
plt.ylim(36, None)

# plot lowest week as a point:
plt.scatter([lowest_week], [lowest_price], marker = 'o', color = 'darkred')
plt.vlines(lowest_week, 0, lowest_price, linestyles = 'dashed', color = 'red')
plt.hlines(lowest_price, 0, lowest_week, linestyles = 'dashed', color = 'red')

# plot highest week as a point:
plt.scatter([highest_week], [highest_price], marker = 'o', color = 'blue')
plt.vlines(highest_week, 0, highest_price, linestyles = 'dashed')
plt.hlines(highest_price, 0, highest_week, linestyles = 'dashed')

# create legends for the points:
legend_elements = [Line2D([0], [0], color = 'darkred', marker = 'o', label = 'Lowest'),
                   Line2D([0], [0], color = 'blue', marker = 'o', label = 'Highest')]

# graph interpretability:
plt.grid(c='lightblue')
plt.xlabel('Week')
plt.ylabel('Price (USD)')
plt.title('AAPL(Apple) 2018 close prices per week')
plt.xticks(list(range(0,56, 10)) + [lowest_week, highest_week])
plt.yticks(list(range(35, 61, 5)) + [lowest_price, highest_price])
plt.legend(handles=legend_elements)
plt.show()
plt.close()


# Ex. 2:
"""display the frequency of the integer price of the closing price per week. """

# obtain list of integer prices
p2_data = [int(x) for x in data_by_week['close'].tolist()]

# create tuples of unique values and frequencies
p2_unique = sorted(list(set(p2_data)))
p2_count = [(i, p2_data.count(i)) for i in p2_unique]

# plotting
plt.bar(range(len(p2_count)), [val[1] for val in p2_count], align='center')
plt.xticks(range(len(p2_count)), [val[0] for val in p2_count])
plt.xticks(rotation=70)
# graph labels
plt.title("AAPL(Apple) 2018 close integer price frequency per week")
plt.xlabel('Price(USD)')
plt.ylabel('Number of Occurrences')
          
plt.show()
plt.close()

import numpy as np #The Numpy numerical computing library
import pandas as pd #The Pandas data science library
import requests #The requests library for HTTP requests in Python
import xlsxwriter #The XlsxWriter libarary for
import math #The Python math module
from scipy import stats #The SciPy stats module
from secrets import IEX_CLOUD_API_TOKEN
from helpers import chunks

portfolio_value = 1000000

stocks = pd.read_csv('sp_500_stocks.csv')
symbol_group = list(chunks(stocks['Ticker'], 100))
symbol_list = []
for i in range(0, len(symbol_group)):
  symbol_list.append(','.join(symbol_group[i]))

my_columns = [
  'Ticker',
  'Price',
  'P/E Ratio',
  'P/E Percentile',
  'P/B Ratio',
  'P/B Percentile',
  'P/S Ratio',
  'P/S Percentile',
  'Number of Shares to Buy'
  ]

value_dataframe = pd.DataFrame(columns = my_columns)

for item in symbol_list:
  batch_api_data = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=advanced-stats,quote&symbols={item}&token={IEX_CLOUD_API_TOKEN}'
  data = requests.get(batch_api_data).json()
  for ticker in item.split(','):
    value_dataframe = value_dataframe.append(
      pd.Series(
        [
          ticker,
          data[ticker]['quote']['latestPrice'],
          data[ticker]['quote']['peRatio'],
          'N/A',
          data[ticker]['advanced-stats']['priceToBook'],
          'N/A',
          data[ticker]['advanced-stats']['priceToSales'],
          'N/A',
          'N/A'
        ],
        index = my_columns
      ),
      ignore_index = True
    )

# Sort by P/E
value_dataframe.sort_values('P/E Ratio', inplace = True)
# Remove the companies with negative P/E ratios
value_dataframe = value_dataframe[value_dataframe['P/E Ratio'] > 0]
# Just use the top 50
value_dataframe = value_dataframe[:50]
# Reset the index
value_dataframe.reset_index(inplace = True)
# Drop the old index
value_dataframe.drop('index', axis=1, inplace = True)

# Calculate the number of shares to buy
number_of_holdings = len(value_dataframe.index)
amount_per_holding = portfolio_value / number_of_holdings
for i in range(0, number_of_holdings):
  price = value_dataframe.loc[i, 'Price']
  value_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(amount_per_holding / price)
print(value_dataframe)
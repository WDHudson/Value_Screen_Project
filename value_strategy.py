import numpy as np #The Numpy numerical computing library
import pandas as pd #The Pandas data science library
import requests #The requests library for HTTP requests in Python
import xlsxwriter #The XlsxWriter libarary for
import math #The Python math module
from scipy import stats #The SciPy stats module
from secrets import IEX_CLOUD_API_TOKEN
from helpers import chunks

stocks = pd.read_csv('sp_500_stocks.csv')

portfolio_value = 1000000
symbol_group = list(chunks(stocks['Ticker'], 100))
symbol_list = []
for i in range(0, len(symbol_group)):
  symbol_list.append(','.join(symbol_group[i]))

my_columns = ['Ticker', 'Price', 'P/E Ratio', 'Number of Shares to Buy']

value_dataframe = pd.DataFrame(columns = my_columns)

for item in symbol_list:
  batch_api_data = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={item}&token={IEX_CLOUD_API_TOKEN}'
  data = requests.get(batch_api_data).json()
  for ticker in item.split(','):
    value_dataframe = value_dataframe.append(
      pd.Series(
        [
          ticker,
          data[ticker]['quote']['latestPrice'],
          data[ticker]['stats']['peRatio'],
          'N/A'
        ],
        index = my_columns
      ),
      ignore_index = True
    )

print(value_dataframe)
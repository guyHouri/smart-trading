#############################################################################
#
# smart trading project - guy houri
#
# includes US stock symbols with market cap > 100 Million, and price above $3. 
# Download the csv file  https://www.nasdaq.com/market-activity/stocks/screener?exchange=nasdaq&letter=0&render=download 
# of all the NYSE, NASDAQ and NYSEAMERICAN public traded companies.
#
#############################################################################


#import and setup
import pandas as pd
import os
import matplotlib.pyplot as plt # for graphs


# get data frame of stocks with market cap > 100 Million, and price above $3
# i downloaded all the stocks from nasdaq in 22/05/2021
def cutStockDatabase():
   stocksDataframe = pd.read_csv(
   r'D:\yudgimel\project\stocks\nasdaq_screener_22052021.csv' ) # turn csv file to pandas dataframe

   stocksDataframe = stocksDataframe.rename(columns={'Market Cap': 'marketCap', 'Last Sale' : 'price', 'Symbol' : 'symbol'}) # rename coloumns
   nasdaqStocks = stocksDataframe[["symbol", "price", "marketCap"]] # take only the coloumns i need

   nasdaqStocks = nasdaqStocks[nasdaqStocks.marketCap > 100000000] # 'remove stocks with market cap below 100 Million

   nasdaqStocks['price'] = nasdaqStocks['price'].str.replace('$','') # in order to change string coloumn to int coloumn we romve $ 
   nasdaqStocks['price'] = nasdaqStocks['price'].astype(float) # change price coloumn to float
   nasdaqStocks = nasdaqStocks[nasdaqStocks.price > 3] # 'remove stocks with market cap below 100 Million


   # turn dataframe to list of alltickers
   nasdaqStocks.drop(['price', 'marketCap'], axis=1, inplace=True) # remove unneccesery coloumns
   alltickers = nasdaqStocks.values.tolist() # turn dataframe to list. it will create list of lists
   alltickers = [''.join(ele) for ele in alltickers] # Convert List of lists to list of Strings using list comprehension + join()
   return alltickers

alltickers = cutStockDatabase()

# includes common words and words used on wsb that are also stock names
blacklist = {'I', 'ARE',  'ON', 'GO', 'NOW', 'CAN', 'UK', 'SO', 'OR', 'OUT', 'SEE', 'ONE', 'LOVE', 'U', 'STAY', 'HAS', 'BY', 'BIG', 'GOOD', 'RIDE', 'EOD', 'ELON', 'WSB', 'THE', 'A', 'ROPE', 'YOLO', 'TOS', 'CEO', 'DD', 'IT', 'OPEN', 'ATH', 'PM', 'IRS', 'FOR','DEC', 'BE', 'IMO', 'ALL', 'RH', 'EV', 'TOS', 'CFO', 'CTO', 'DD', 'BTFD', 'WSB', 'OK', 'PDT', 'RH', 'KYS', 'FD', 'TYS', 'US', 'USA', 'IT', 'ATH', 'RIP', 'BMW', 'GDP', 'OTM', 'ATM', 'ITM', 'IMO', 'LOL', 'AM', 'BE', 'PR', 'PRAY', 'PT', 'FBI', 'SEC', 'GOD', 'NOT', 'POS', 'FOMO', 'TL;DR', 'EDIT', 'STILL', 'WTF', 'RAW', 'PM', 'LMAO', 'LMFAO', 'ROFL', 'EZ', 'RED', 'BEZOS', 'TICK', 'IS', 'PM', 'LPT', 'GOAT', 'FL', 'CA', 'IL', 'MACD', 'HQ', 'OP', 'PS', 'AH', 'TL', 'JAN', 'FEB', 'JUL', 'AUG', 'SEP', 'SEPT', 'OCT', 'NOV', 'FDA', 'IV', 'ER', 'IPO', 'MILF', 'BUT', 'SSN', 'FIFA', 'USD', 'CPU', 'AT', 'GG', 'Mar'}


# adding wsb/reddit flavour to vader to improve sentiment analysis, score: 4.0 to -4.0
new_words = {
    'trash': -4.0,
    'garbage': -4.0,
    'citron': -4.0,  
    'hidenburg': -4.0,    
    'rocket': 4.0,  
    'moon': 4.0,
    'highs': 2.0,
    'mooning': 4.0,
    'long': 2.0,
    'short': -2.0,
    'call': 4.0,
    'calls': 4.0,    
    'put': -4.0,
    'puts': -4.0,    
    'break': 2.0,
    'tendie': 2.0,
     'tendies': 2.0,
     'town': 2.0,     
     'overvalued': -3.0,
     'undervalued': 3.0,
     'buy': 4.0,
     'sell': -4.0,
     'gone': -1.0,
     'gtfo': -1.7,
     'paper': -1.7,
     'bullish': 3.7,
     'bearish': -3.7,
     'bagholder': -1.7,
     'stonk': 1.9,
     'green': 1.9,
     'money': 1.2,
     'print': 2.2,
     'rocket': 2.2,
     'bull': 2.9,
     'bear': -2.9,
     'pumping': -1.0,
     'sus': -3.0,
     'offering': -2.3,
     'rip': -4.0,
     'downgrade': -3.0,
     'upgrade': 3.0,     
     'maintain': 1.0,          
     'pump': 1.9,
     'hot': 1.5,
     'drop': -2.5,
     'rebound': 1.5,  
     'crack': 2.5,}

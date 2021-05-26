#############################################################################
#
# smart trading project - guy houri
#
# main stock class. import all mosoules and classes to here and use them on the stock
#
#############################################################################


import numpy as np
from numpy.lib.function_base import percentile
import pandas as pd
import matplotlib.pyplot as plt # for graphs
from datetime import datetime

from PIL import Image
import io
import base64
 
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import yfinance as yf   

import sys
sys.path.append(r"D:\yudgimel\project")
from stocks import myDate

from stocks import movingAverage1
from stocks import portofolio
from stocks import trends
from stocks import yahooScraper

import os
from pathlib import Path

"""
        
"""

start_date, end_date = myDate.getDateToday()
dt_of_now = myDate.getDateTimeNow()
#alphavntage
API_key = 'LMP6ND8IA11NAI2D'
ts = TimeSeries(key=API_key,output_format='pandas') # create time series object. pandas is output fromat
ti = TechIndicators(key=API_key, output_format='pandas') #technical indicaters

class Stock:

    def __init__(self, name):
        self.name = name
        self.title = name+' stock'
        
        self.botPlace = r"D:/yudgimel/project/website/static/images/bot/"+name+dt_of_now+'.png'
        
        self.data, self.meta = ts.get_monthly_adjusted(name) # data - tpe dataframe
        self.data = self.data.rename(columns={'1. open': 'open'})
        self.data = self.data.rename(columns={'2. high': 'high'})
        self.data = self.data.rename(columns={'3. low': 'low'})
        self.data = self.data.rename(columns={'4. close': 'close'})
        self.data = self.data.rename(columns={'5. adjusted close': 'adjusted close'})
        self.data = self.data.rename(columns={'6. volume': 'volume'})
        self.data = self.data.rename(columns={'7. dividend amount': 'dividend amount'})
        
        self.data = self.data[(self.data.index > start_date) & (self.data.index <= end_date)]
        self.data = self.data.sort_index(ascending=True)

        
        # set indicators
        self.closing_prices = self.data.close # 'pandas.core.series.Series'
        self.MACD_indicator = movingAverage1.movingAvg(self.closing_prices) #dataframe
        self.MACD_line, self.signal_line, self.histogram = self.MACD_indicator.MACD() # 

        # more indicators from web scraping
        self.scraper = yahooScraper.Scraper(self.name)

        # set google trends
        self.trend = trends.Trend(self.name, '12-m')
        self.trend.build()
        self.trend.interestOverTime()

        #set sentiment
        self.sentiment_anylasise_png = ''
        self.mentioned_picks_png = ''

    
    def trendsGraph(self):
        #google trends Graph
        fig, (ax2) = plt.subplots(1)
        ax2.plot(self.trend.interest,label = 'interest', color = 'black')
        ax2.legend(loc='lower left') # legend is an area describing the elements of the graph.
        ax2.title.set_text('1 year '+self.name+' search by interest')
        ax2.set(xlabel='Date', ylabel=self.name+' stock search interest')
        # save graph as png
        self.trends_fig_place = r'stocks/trendFigs/' 
        self.trends_fig_place = self.trends_fig_place +dt_of_now+ self.name+'.PNG'
        plt.savefig(self.trends_fig_place)


    def getLatestPng(self):
        dirpath=r'D:\yudgimel\project\stocks\sentimentFigs'
        paths = sorted(Path(dirpath).iterdir(), key=os.path.getmtime)
        self.sentiment_anylasise_png =  str(paths[-1])
        self.mentioned_picks_png =  str(paths[-2])


    def redditSentiment(self):
        from stocks import redditSentiment
        # reddit sentiment
        self.sentiment_anylasise_png = redditSentiment.sentiment_anylasise_fig_place
        self.mentioned_picks_png = redditSentiment.mentioned_picks_fig_place


    def createGraphorig(self):
        plt.rcParams["figure.figsize"]  = [16,9] # size of graph
        plt.rcParams["lines.linewidth"] = 0.75   # lines width
        plt.rcParams.update({'font.size': 22})   # font size

        fig, (ax1, ax2) = plt.subplots(2) # Create a figure and a set of subplots

        # subplot 1 - shows where to buy and sell (based on where MACD and signal line meet)
        ax1.plot(self.closing_prices, label = 'Closing Prices') # add closing_prices line to graph
        ax1.plot(self.MACD_indicator.EMA(12), 'r', label = '12 day EMA') #  plot the 12 day EMA 
        ax1.plot(self.MACD_indicator.EMA(26), 'y', label = '26 day EMA') #  plot the 26 day EMA 
        ax1.legend(loc='lower left') # legend is an area describing the elements of the graph.
        ax1.title.set_text('graph price with moving avarage')
        ax1.set(xlabel='Date', ylabel=self.title+'price')

        # subplot 2 
        ax2.plot(self.MACD_line, label = 'MACD Line')
        ax2.plot(self.signal_line, label = 'Signal Line')
        histogram_y = [self.histogram['EMA'].iloc[i] for i in range(0, len(self.histogram))]
        # green if histogram is above zero and red if hhistogram is below zero
        ax2.bar(self.histogram.index, histogram_y, color=['g' if histogram_y[i] > 0 else 'r' for i in range(0,len(histogram_y))], width = 1, label = 'Histogram')
        ax2.legend(loc='lower left')
        ax2.set(xlabel='Date', ylabel=self.title+'price')

        
        #save plt
        self.price_fig_place = r'D:/yudgimel/project/website/static/images/stock/'+self.name+ dt_of_now+'price.PNG'
        plt.savefig(self.price_fig_place, bbox_inches='tight')

        price_fig_place = self.price_fig_place.find('static') - 1
        self.price_fig_place_html = self.price_fig_place[price_fig_place:]
        


    def showCreateGraphOrig(self):
        fig = self.createGraphorig()
        plt.show()

    # we get data frame of stock in the last year
    def buySell(self, porto):

        self.buypd= pd.DataFrame(index=self.closing_prices.index, columns=['Buy']) # an empty data-frame to store buy signals
        self.sellpd = pd.DataFrame(index=self.closing_prices.index, columns=['Sell']) # an empty data-frame to store sell signals

        dataFrameClosingPrices = self.closing_prices.to_frame() 

        for i in range(1, len(self.closing_prices)): 

            today_macd = self.MACD_line['EMA'].iloc[i]
            today_signal_line = self.signal_line['EMA'].iloc[i]
            today_close_price = self.closing_prices[i]
            date = dataFrameClosingPrices.index[i]
            soldHalf = False

            if i==1:
                if today_macd > today_signal_line:
                    high = "macd"
                     #buy
                    self.buypd.iloc[i] = today_close_price
                    porto.buy(today_close_price, date, porto.botMoney/5)
                else:
                    high="signal"
            elif today_macd > today_signal_line and high =="signal": # if we start when macd is above we buy
                if porto.botMoney>porto.transactionFees*15: # have money
                    #buy
                    self.buypd.iloc[i] = today_close_price
                    porto.buy(today_close_price, date, porto.botMoney/5)
                    high="macd"

            elif today_macd < today_signal_line and high=="macd":
                if porto.shares > 0: # we have stocks
                    self.sellpd.iloc[i] = self.closing_prices[i] # SELL
                    sellpercentage = 1
                    porto.sell(today_close_price,sellpercentage, date)
                    high=="signal"

            if porto.shares > 0: # we have stocks
                if porto.lastPriceBaught*0.70>today_close_price: # 70% loss we sell all
                    self.sellpd.iloc[i] = self.closing_prices[i] # SELL
                    sellpercentage = 1
                    porto.sell(today_close_price,sellpercentage, date)

        #end trade sessiom
        if porto.shares>0: # if still left ahres sell them
            self.sellpd.iloc[i] = self.closing_prices[i] # SELL
        porto.endTradeSession(today_close_price,date) # end trade session sells all stocks

        # Plotting results 
        plt.rcParams["figure.figsize"] = [16,9] # size of graph
        plt.rcParams["lines.linewidth"] = 0.75

        fig, (ax1, ax2) = plt.subplots(2) # Create a figure and a set of subplots

        # subplot 1 - shows where to buy and sell (based on where MACD and signal line meet)
        ax1.plot(self.closing_prices, label = 'Closing Prices') # add closing_prices line to graph
        ax1.plot(self.buypd, 'g^', label = 'Buy')
        ax1.plot(self.sellpd, 'rv', label = 'Sell')
        ax1.plot(self.MACD_indicator.EMA(12), 'r', label = '12 day EMA') #  plot the 12 day EMA 
        ax1.plot(self.MACD_indicator.EMA(26), 'y', label = '26 day EMA') #  plot the 26 day EMA 
        ax1.legend(loc='upper left') # legend is an area describing the elements of the graph.
        ax1.title.set_text('buy and sell based on histogarm')
        ax1.set(xlabel='Date', ylabel='($) AUD stock')

        # subplot 2 
        ax2.plot(self.MACD_line, label = 'MACD Line')
        ax2.plot(self.signal_line, label = 'Signal Line')
        histogram_y = [self.histogram['EMA'].iloc[i] for i in range(0, len(self.histogram))]
         # green if histogram is above zero and red if hhistogram is below zero
        ax2.bar(self.histogram.index, histogram_y, 
        color=['g' if histogram_y[i] > 0 else 'r' for i in range(0,len(histogram_y))],
        width = 1, label = 'Histogram')
        ax2.legend(loc='lower left')
        ax2.set(xlabel='Date', ylabel='($) AUD')

        plt.savefig(self.botPlace, bbox_inches='tight')
        print('saved')


    def buy(self, porto, today_close_price, buyDate):
        buyPrice =  today_close_price
        purchase_money = porto.botMoney/5 
        shares = purchase_money/buyPrice
        stockToBuy = portofolio.stock_baught(self.name, buyPrice, shares, buyDate)
        porto.buyStock(stockToBuy)
        return stockToBuy

    def sell(self, porto, today_close_price, stockToBuy, sellpercentage, sellDate):
        porto.sellStock(stockToBuy, today_close_price, sellDate, sellpercentage)

    def sellAll(self, porto, today_close_price, sellDate):
        porto.sellAll(today_close_price,  sellDate)
        

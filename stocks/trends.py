#############################################################################
#
# smart trading project - guy houri
#
# create google trends graph
#
#############################################################################

from os import name
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt # for graphs

from datetime import datetime

now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d%m%Y%H%M%S")

pytrends = TrendReq(hl='en-US') # language

class Trend:
    def __init__(self, ticker, timeframe):
        # vars
        self.keyWords = []
        self.keyWords.append(ticker)
        self.name      = ticker
        self.timeframe = 'today '+timeframe # fromat like 12-m, 5-y
        self.geo       = 'GB'
        self.interest  = None
        

    def build(self):
        pytrends.build_payload(self.keyWords, timeframe=self.timeframe,  geo=self.geo)


    def interestOverTime(self):
        self.interest = pytrends.interest_over_time()
        self.interest = self.interest.drop('isPartial', axis=1)

        self.lastTimestamp = self.interest.index[-1]
        self.lastValue     = self.interest[self.name][-1]

        # check if now it is trending more
        value = self.interest[self.name]
        sum=0
        count=0
        for i in value:
            count+=1
            sum+=i

        memuza = sum/count
        if(self.lastValue>memuza+5):
            self.talkedAbout = 'stock is talked about beyond the average !'
        else:
            self.talkedAbout = "stock is not so hot right now. it is below the average searches. but maybe for you it is good thing ;)"
        
        self.trends_fig_place_html = ''


    def getStockGraph(self):
        from datetime import date
        from datetime import datetime

        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d%m%Y%H%M%S")

        today = date.today()
        strToday = str(today.strftime('%Y-%m-%d'))
        yearAgo = date(today.year - 1, today.month, today.day)
        strYearAgo = str(yearAgo.strftime('%Y-%m-%d'))
        start_date = strYearAgo
        end_date = strToday

        #alphavntage
        from alpha_vantage.timeseries import TimeSeries

        API_key = 'LMP6ND8IA11NAI2D'
        ts = TimeSeries(key=API_key,output_format='pandas') # create time series object. pandas is output fromat

        df, meta = ts.get_monthly_adjusted(self.name) # data - tpe dataframe
        df = df.rename(columns={'4. close': 'Close'})
        df = df[(df.index > start_date) & (df.index <= end_date)]
        self.df = df.sort_index(ascending=True)



    def saveGraphfigInStatics(self):
         # save fig
        plt.rcParams["figure.figsize"] = [16,9] # size of graph
        plt.rcParams["lines.linewidth"] = 0.75
        plt.rcParams.update({'font.size': 22})   # font size
        

        fig, (ax1, ax2) = plt.subplots(2)
        #ax1 - trends figure
        ax1.plot( self.interest,label = 'interest', color = 'black')
        ax1.legend(loc='lower left') # legend is an area describing the elements of the graph.
        ax1.title.set_text('1 year '+self.name+' search by interest')
        ax1.set(xlabel='Date', ylabel=self.name+' stock search interest')

        #ax2 - compare to stock graph
        self.getStockGraph()
        ax2.plot(self.df['Close'],label = 'close price history',alpha=1) # show 

        fig.patch.set_linewidth(10)
        fig.patch.set_edgecolor('black')

        trends_fig_place = r'D:\yudgimel\project\website\static\images\trends\trend' 
        trends_fig_place = trends_fig_place +dt_string+ self.name+'.PNG'
        print('\n', trends_fig_place)
        plt.savefig(trends_fig_place, bbox_inches='tight')

        find = trends_fig_place.find('static') - 1
        self.trends_fig_place_html = trends_fig_place[find:]

"""
mytrend = Trend('amzn', '12-m')
mytrend.build()
mytrend.interestOverTime()
mytrend.saveGraphfigInStatics()
"""
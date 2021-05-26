from matplotlib import pyplot as plt
from portofolio import Portofolio
from portofolio import Portofolio
from portofolio import newPorto
from stock import Stock


money_in_portofolio = 20000
bot_money = 5000
porto = newPorto(money_in_portofolio, bot_money)

stock_ticker = 'teva'
myStock = Stock(stock_ticker)
myStock.buySell(porto)

"""import matplotlib.pyplot as plt
import matplotlib.image as mpimg

#trends
img = mpimg.imread(myStock.trends_fig_place)
imgplot = plt.imshow(img)
plt.show()"""



"""
        self.trend = trends.Trend(self.name, '12-m')
        self.trend.build()s
        self.trend.interestOverTime()

        ax1.plot(self.trend.interest,label = 'interest', color = 'blue')
        ax1.legend(loc='lower left') # legend is an area describing the elements of the graph.
        ax1.title.set_text(self.name+' search by interest compared to closing prices')
        
"""
import itertools
from datetime import date
from math import log

class stock_baught():
    
    id=0

    def __init__(self, ticker, price, shares, buyDate):
        self.ticker = ticker
        self.buyDate =  buyDate.strftime("%d/%m/%Y, %H:%M:%S")
        self.price = price
        self.shares = shares
        self.objID=stock_baught.id
        self.moneyInShares = self.shares*self.price
        stock_baught.id=stock_baught.id+1

    def check_profit15(self, price):
        if(self.price*1.15<price):
            return 1
        return 0


class Portofolio():

    transactionFees = 5.50

    def __init__(self, balance, botMoney):
        self.startBalance = balance
        self.balance = balance
        self.botMoney = botMoney # money for bot to invest
        self.stocks = []
        self.log_index=0
        self.log = []

    def buyStock(self, stockBaught):
        self.stocks.append(stockBaught)
        self.balance=self.balance-stockBaught.price-Portofolio.transactionFees
        self.botMoney=self.botMoney-stockBaught.price-Portofolio.transactionFees

        # write in log
        text = "baught stock "+str(stockBaught.id)+" "+str(stockBaught.ticker)+" in date "+str(stockBaught.buyDate)+" at price "+str(stockBaught.price)+" so i have "+str(stockBaught.shares)+" shares"+" . balance =  "+str(self.balance)
        self.log.append(text)

    def sellStock(self, stockBaught, currentPrice, sellDate, sellPercentage):
         j=0
         for i in self.stocks:
            if i.objID==stockBaught.objID:
                if sellPercentage==1:
                    self.stocks.remove(i)
                    j=j-1
                else:
                    self.stocks[j].shares=self.stocks[j].shares/2
                self.botMoney=self.botMoney-Portofolio.transactionFees+currentPrice*(sellPercentage)
                self.balance=self.balance-Portofolio.transactionFees+currentPrice*(sellPercentage)

                # write in log
                text = "sold " + str(sellPercentage) + " percent of stock " + str(stockBaught.id) + " " + str(i.ticker) + "when it was "+str(currentPrice)+ " in date " +str(sellDate)+ str(currentPrice-stockBaught.price)  + " . balance =  " +str(self.balance)  
                self.log.append(text)   
         j = j+1

    def sellAll(self, today_close_price, date):
        # sell all stocks
        sellPercentage = 1
        for i in self.stocks:
            self.sellStock(i, today_close_price, date, sellPercentage)


    def endTradeSession(self, date, today_close_price):

        self.sellAll(today_close_price, date)

        # print log
        for i in range(len(self.log)):
            print("\n",self.log[i])

        # print results
        print("\n started with ",str(self.startBalance)," and finished at ", str(self.balance))
        
        # change start balance to current balance
        self.startBalance=self.balance


class newPorto:
    def __init__(self, money, botMoney):
        self.startMoney = money
        self.money = money
        self.botMoney = botMoney
        self.shares=0
        self.moneyInvested=0
        self.transactionFees = 9.5
        self.log = []
        self.lastPriceBaught =1000000

    def buy(self, stockPrice, date, moneyToInvest):
        self.money = self.money-self.transactionFees-moneyToInvest
        self.botMoney = self.botMoney-self.transactionFees-moneyToInvest
        self.moneyInvested = self.moneyInvested-self.transactionFees+moneyToInvest
        sharesBaught = moneyToInvest/stockPrice
        self.lastPriceBaught = stockPrice
        
        date = date.strftime("%d/%m/%Y, %H:%M:%S")
        self.shares+=sharesBaught
        logstr = "acount balance " + str(self.money)+ ". baugth "+str(self.shares)+" shares."+" stock. cost " + str(stockPrice) + " . in date " + str(date) + " . i spent " + str(moneyToInvest)
        self.log.append(logstr)

    def sell(self, stockPrice, sellPercentage, date ):
        self.botMoney = self.botMoney + self.shares*sellPercentage*stockPrice-self.transactionFees
        self.money = self.money + self.shares*sellPercentage*stockPrice-self.transactionFees
        self.moneyInvested = self.moneyInvested - self.shares*sellPercentage*stockPrice-self.transactionFees
        startshares = self.shares
        self.shares = self.shares - self.shares*sellPercentage

        date = date.strftime("%d/%m/%Y, %H:%M:%S")
        got =  self.shares*sellPercentage*stockPrice
        percentage=sellPercentage*100
        logstr =  str("acount balance ")+str(self.money)+ ". sold "+str(startshares)+" shares. " +"stock. cost " + str(stockPrice) + " . in date " + str(date) + " . i got " + str(got) + " . sold "+str(percentage) +" percent of stock"
        self.log.append(logstr)

    def endTradeSession(self, stockPrice, date):
        self.sell(stockPrice, 1, date)
        #print
        for i in range(len(self.log)):
            print("\n",self.log[i])
        print("strted with: ", self.startMoney, ". ended with: ", self.money)
        
        
"""
today = date.today()
strToday = str(today.strftime('%Y-%m-%d'))
yearAgo = date(today.year - 1, today.month, today.day)
if today.month-6 < 0:
    print(today.month)
    month = 12-today.month
else:
    month = today.month-6

monthAgo = date(today.year, month, today.day)

porto = newPorto(20000, 5000)
porto.buy(100 ,yearAgo, 1000)
porto.buy(110, monthAgo, 500)
porto.endTradeSession(  150, date.today())
"""
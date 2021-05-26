#############################################################################
#
# smart trading project - guy houri
#
# yahoo finance wont bring me all the data i want. so i go to the internet and take the data needed
# class scraper Extract financial data from Yahoo! Finance using background java strings and a hidden api.
#
#############################################################################

import math
import re
import json
import csv
from io import StringIO
from bs4 import BeautifulSoup
import requests

class Scraper:
    #                  stock - name of stock i want to scrape
    def __init__(self, stock):

        # url values
        self.url_stats      = 'https://finance.yahoo.com/quote/{}/key-statistics?p={}'
        self.url_profile    = 'https://finance.yahoo.com/quote/{}/profile?p={}'
        self.url_financials = 'https://finance.yahoo.com/quote/{}/financials?p={}'


        # get data from yahoo / finance - explained deeply in yahoo-finance-scraper

        response = requests.get(self.url_financials.format(stock, stock))
        soup = BeautifulSoup(response.text, 'html.parser')
        pattern = re.compile(r'\s--\sData\s--\s')
        script_data = soup.find('script', text=pattern).contents[0]
        start = script_data.find("context")-2
        json_data = json.loads(script_data[start:-12])

        #get stock price
        self.price = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['price']['regularMarketPrice']['raw']


        # get data from yahoo / statistics - explained deeply in yahoo-finance-scraper

        # request the webpage, passing in the stock variable to fill in the url template
        # extract the html using BeautifulSoup
        response = requests.get(self.url_stats.format(stock, stock))
        soup = BeautifulSoup(response.text, 'html.parser') 

        # there is a javascript function, appropriately commented with "--Data--".
        # i can use regular expressions with BeautifulSoup in order to identify the script tag with the function i am looking for.
        pattern = re.compile(r'\s--\sData\s--\s')
        script_data = soup.find('script', text=pattern).contents[0]

        # slice data to start and end point
        # data is in javascript function so we move it to json file
        start = script_data.find("context")-2
        json_data = json.loads(script_data[start:-12]) # json - java script object notation(=סימון)

        # set vars from statistics
        # EPS _____ lower is better
        self.earningsPerShare = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']['trailingEps']['raw']
        # P / E  _____ lower is better
        self.priceToEarnings = self.price / self.earningsPerShare
        # EV
        self.enterpriseValue = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']['enterpriseValue']['raw']
      
        # EV / R _____ lower = better
        self.enterpriseValueToReveneu = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']['enterpriseToRevenue']['raw']
        # PM _____ 0.35 = 35% ____ high = better# PEG _____ price to earnings _____ 
        self.profitMargin = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']['profitMargins']['raw'] 
        # 5-years PEG _____ lower than 1 is better
        self.priceToEarningsGrowth = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']['pegRatio']['raw']
        # EV / EBITDA _____ 11 < s%p500 > 14 lower is better
        self.enterpriseValueToEbitda = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']['enterpriseToEbitda']['raw']
        # EQG _____ higher is better _____ 0.97 = 97%. 
        self.earningsQuaterlyGrowth = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['defaultKeyStatistics']['earningsQuarterlyGrowth']['raw']


        # calculte stock value by formula
        # formula by asaf ravid
        self.asafravid =  ( ( self.enterpriseValueToReveneu * self.priceToEarnings * self.enterpriseValueToEbitda ) / self.profitMargin ) * ( (math.sqrt(self.priceToEarningsGrowth)) / self.earningsQuaterlyGrowth ) #* self.enterprisevalueToCashflowoperationsEffective


    def printIndicators(self):
        print("earningsPerShare - ", self.earningsPerShare)
        print("pricesToEarnings - ", self.priceToEarnings)
        print("enterpriseValue - ", self.enterpriseValue)

        print("enterpriseValueToReveneu - ", self.enterpriseValueToReveneu)
        print("profitMargin - ", self.profitMargin)
        print("priceToEarningsGrowth - ", self.priceToEarningsGrowth)

        print("enterpriseValueToEbitda - ", self.enterpriseValueToEbitda)
        print("earningsQuaterlyGrowth - ", self.earningsQuaterlyGrowth)
        #print("enterprisevalueToCashflowoperationsEffective - ", self.enterprisevalueToCashflowoperationsEffective)


        print('asaf ravid value = ', self.asafravid )


"""
scraping = Scraper('fb')
scraping.printIndicators()
"""
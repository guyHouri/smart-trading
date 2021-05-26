#############################################################################
#
# smart trading project - guy houri
# website
# here i write the functions of the website
#
#############################################################################

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect

import sys

import requests
sys.path.append(r"D:\yudgimel\project\website\main")
sys.path.append(r"D:\yudgimel\project\website\main\templates")
sys.path.append(r"D:\yudgimel\project")

import forms
from stocks import stock
from stocks import trends

def home(request):
    print('\n in home \n')

    if request.method == 'POST':
        print('\n post \n')
        form = forms.tikerForm(request.POST) # put in the data the user entered
        if form.is_valid():
            ticker = request.POST['ticker']
            print('\n is valid - returnin to ticker')
            return HttpResponseRedirect(ticker) # www.myapp/ticker
    else:
        print('\n post \n')
        form = forms.tikerForm()
    return render(request, "main/home.html", {'form':form})


def ticker(request, tid): #tid = ticker 
    print('\n in ticker,  tid = ', tid, ' \n')

    #stock
    if tid =='redditsentiment':
        print('\n in sentiment \n')

        context  = {} 
        context['5sentiment'] = r"/static/images/redditSen/5analyasise.png"
        context['10talked'] = r"/static/images/redditSen/10mentioned.png"

        return render(request, 'main/sentiment.html', context)
    else:
        try:
            myStock = stock.Stock(tid)
    
        except ValueError:
            return render(request, "main/wrongticker.html")

        myStock.createGraphorig()

        # creating dictionary
        context = {} # 
        context['ticker'] = myStock.title
        context['stockPrice'] = myStock.scraper.price
        context['pricepng'] = myStock.price_fig_place_html
        context['trendsurl'] = tid+'/googletrends'

        request.session['ticker'] = tid

        return render(request, "main/ticker.html", context)


def trendsBotton(request, tid):
    print('\n in trends \n')
    # creating dictionary
    context = {}
    ticker = context['ticker'] = request.session['ticker']
    # getting trend data
    myTrend = trends.Trend(ticker, '12-m')
    myTrend.build()
    myTrend.interestOverTime()
    myTrend.saveGraphfigInStatics()
    # more values to dictaionary
    context['trendsPng'] = myTrend.trends_fig_place_html
    context['talkedAbout'] = myTrend.talkedAbout
    
    return render(request, "main/trends.html", context)


def sentimentBotton(request):
    print('\n in sentiment \n')

    context  = {} 
    context['5sentiment'] = r"/static/images/redditSen/5analyasise.png"
    context['10talked'] = r"/static/images/redditSen/10mentioned.png"

    return render(request, 'main/sentiment.html', context)


#############################################################################
#
# smart trading project - guy houri
# website
# here i write for each adress to activate a certain function
# for example: .../website/ticker - will activate function to get stock details
#
#############################################################################
from . import views
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('<str:tid>', views.ticker, name='ticker'),
    path('', views.home, name="home"),
    path('<str:tid>/googletrends', views.trendsBotton, name="script"),
    path('redditsentiment', views.sentimentBotton, name="script"),
    path('wrongticker', views.home, name="home1"),
    #path('website/<str:tid>/googletrends', views.trendsBotton, name="script"),
]
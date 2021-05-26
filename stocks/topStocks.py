#import and setup
import pandas as pd
import os
import matplotlib.pyplot as plt # for graphs

stocks = pd.read_csv(
   'D:\yudgimel\project\stocks\db.csv',
   parse_dates=True,
   dayfirst=True ) # required as dates in csv are DD/MM/YYYY 

#value = stocks['sss_value']

evr = stocks['enterprise_value_to_revenue']

for i in range(0, len(stocks)):
    a = stocks['enterprise_value_to_revenue'].iloc[i]
    print(a)
    

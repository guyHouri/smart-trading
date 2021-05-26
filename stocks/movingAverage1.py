import pandas as pd
from stocks import myDate

start_date, end_date = myDate.getDateToday()

class movingAvg():
    def __init__(self, closing_prices):
        self.data = pd.DataFrame(closing_prices)

    # This implementation sets the default averaging length to 50 days 
    # returns a data-frame of the averaged prices with their corresponding date index
    # calculate 50 days 
    def EMA(self, averaging_length=50):
        ret = self.data.ewm( span=averaging_length, adjust=False).mean()
        return ret.rename(columns={'close': 'EMA'})

    # calculate the MACD line, signal line and histogram
    def MACD(self, a=12, b=26, c=9):
        MACD_line = self.EMA(a) - self.EMA(b)
        signal_line = MACD_line.ewm(span=c, adjust=False).mean()
        histogram = MACD_line - signal_line
        return MACD_line, signal_line, histogram

    
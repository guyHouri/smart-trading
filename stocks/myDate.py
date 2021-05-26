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

def getDateToday():
    return start_date, end_date

def  getDateTimeNow():
    return dt_string

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import sys
sys.path.append(r"D:\yudgimel\project")
from stocks import stock

stock_ticker = 'msft'
my_stock = stock.Stock(stock_ticker)
stock_fig = my_stock.saveGraph()

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1('dash tutorials'),
    html.Img(id='example')
    ]) 

if __name__ == '__main__':
    app.run_server(debug=True)
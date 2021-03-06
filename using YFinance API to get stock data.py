!pip install yfinance==0.1.67
!pip install pandas==1.3.3
!pip install requests==2.26.0
!pip install bs4
!pip install plotly==5.3.1
!pip install html5lib==1.1 

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#-------------Graphing Function--------------
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

#--------------Tesla--------------------
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period='max')
tesla_data.reset_index(inplace=True)
tesla_data.head()
url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text
soup = BeautifulSoup(html_data, 'html5lib')
tesla_html = pd.read_html(url)
tesla_revenue = tesla_html[1]
tesla_revenue.rename(columns={'Tesla Quarterly Revenue(Millions of US $)':'Date','Tesla Quarterly Revenue(Millions of US $).1':'Revenue'},inplace=True)
tesla_revenue.head()
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
tesla_revenue.tail()


#--------------------------------------GME-------------------------
gme = yf.Ticker("GME")
gme_data = gme.history(period='max')
gme_data.reset_index(inplace=True)
gme_data.head()
url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
html_data = requests.get(url).text
soup = BeautifulSoup(html_data, 'html5lib')
gme_html = pd.read_html(url)
gme_revenue = gme_html[1]
gme_revenue.rename(columns={'GameStop Quarterly Revenue(Millions of US $)':'Date','GameStop Quarterly Revenue(Millions of US $).1':'Revenue'},inplace=True)
gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"")
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
gme_revenue.head()
gme_revenue.tail()

#--------------------Graphs------------------------
make_graph(tesla_data, tesla_revenue, 'Tesla')

make_graph(gme_data,gme_revenue,'GameStop')


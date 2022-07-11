import json, requests, sqlite3
import pandas as pd
#headers =

data_url = "https://data.alpaca.markets/v1/bars/1Min?symbols="

#Specify the tickers
tickers = ['AAPL','AMZN','FB','GOOG','NFLX']
symbols = ",".join(tickers)

r=requests.get()



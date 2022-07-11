import json, requests, sqlite3
import pandas as pd

headers = json.loads(open('Alpaca_Key.txt','r').read())
data_url = "https://data.alpaca.markets/v1/bars/1Min?symbols="

#Specify the tickers
tickers = ['AAPL','AMZN','FB','GOOG','NFLX']
symbols = ",".join(tickers)

r = requests.get(f'{data_url}{symbols}',headers=headers)
data = r.json()
print(data)
#Establish database connection
#db = sqlite3.connect("alpaca/minutes.db")

#Define a create table function



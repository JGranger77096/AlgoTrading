# Step 2

import json, requests, sqlite3
import pandas as pd
import ssl_patch
import alpaca_trade_api as tradeapi

headers = json.loads(open('Alpaca_Req.txt','r').read())
data_url = 'https://data.alpaca.markets/v2/stocks/bars/1Hour?symbols='

# Specify the tickers
tickers = ['AAPL','AMZN','FB','GOOG','NFLX']
symbols = ",".join(tickers)

#lines below don't work
#r = requests.get(f'{data_url}{symbols}', headers=headers, verify=False)
#print('r.content: ', r.content)
#data = r.json()

#Create empty dataframe
hist_df = pd.DataFrame()

# Try alternative approach to collect historical data, as code above doesn't work for me (7/15/22)
with ssl_patch.no_ssl_verification():
    api = tradeapi.REST(key_id=headers['APCA-API-KEY-ID'],
                            secret_key=headers['APCA-API-SECRET-KEY'],
                            base_url="https://data.alpaca.markets",
                            api_version='v2')

    for ticker in tickers:
        ticker_df = api.get_bars(ticker,'1Min').df
        ticker_df['stock'] = ticker
        hist_df = hist_df.append(ticker_df)
hist_df['timestamp'] = pd.DatetimeIndex(pd.to_datetime(hist_df.index, unit='s',))
print(hist_df.info())
hist_df.to_csv('alpaca_multibars.csv')

# Establish database connection
db = sqlite3.connect("minutes.db")

# Define a create table function
def create_table(symbols):
    cursor = db.cursor()
    for symbol in symbols:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {symbol} (timestamp DATETIME PRIMARY KEY, open real(15,5), high REAL(15,5), low REAL(15,5), volume INTEGER)")
        try:
            db.commit()
        except:
            db.rollback()

# Create a table for each stock
create_table([ticker for ticker in tickers]) #list comprehension

# Load data into tables
hist_df.to_sql(name='hist_data_min', con=db, if_exists='append', index=False)
db.commit()

# Check database data - write to file
from_db = pd.read_sql(con=db,sql='SELECT * FROM hist_data_min')
from_db.to_csv("from_db.csv")

db.close()
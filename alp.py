# Step 1
# Import alpaca trade API, play with functions
import datetime

import ssl_patch
import json
import alpaca_trade_api as tradeapi
import pandas as pd
from datetime import timedelta

headers = json.loads(open('Alpaca_Key.txt','r').read())

with ssl_patch.no_ssl_verification():
    api = tradeapi.REST(key_id=headers['APCA-API-KEY-ID'],
                        secret_key=headers['APCA-API-SECRET-KEY'],
                        base_url=headers['APCA_API_BASE_URL'],
                        api_version='v2')
    #Specify FAANG Stocks
    symbols=['AAPL','AMZN','FB','GOOG','NFLX']

    #Get historical data
    delta = datetime.timedelta(days=5)
    end = datetime.datetime.fromtimestamp(api.get_clock().next_close.timestamp())
    start = end-delta
    print(start.isoformat())

    #barsets = api.get_bars(symbols,'1D', start=start.isoformat(), end=end.isoformat()).df
    barsets = api.get_bars(symbols, '1D').df

    barsets.to_csv('alpaca_bars.csv')

    #Get account status
    account = api.get_account()
    print(account)

    #List all active assets available to trade
    active_assets = api.list_assets(status='active')
    active_assets_df = pd.DataFrame(active_assets)
    active_assets_df.to_csv('alpaca_active_assets.csv')
    print(active_assets[-1])

    #Get clock
    print(api.get_clock())
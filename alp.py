# Step 1
# Import alpaca trade API

import ssl_patch
import json
import alpaca_trade_api as tradeapi
import pandas as pd

headers = json.loads(open('Alpaca_Key.txt','r').read())

with ssl_patch.no_ssl_verification():
    api = tradeapi.REST(key_id=headers['APCA-API-KEY-ID'],
                        secret_key=headers['APCA-API-SECRET-KEY'],
                        base_url=headers['APCA_API_BASE_URL'],
                        api_version='v2')
    #Specify FAANG Stocks
    symbols=['AAPL','AMZN','FB','GOOG','NFLX']

    #Get historical data
    barsets = api.get_bars(symbols,'1D').df
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
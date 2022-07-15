# Step 5: update stock price table programmatically

import sqlite3
import ssl_patch
import alpaca_trade_api as tradeapi
import json
import pandas as pd
from  datetime import date

headers = json.loads(open('Alpaca_Key.txt','r').read())

with ssl_patch.no_ssl_verification():
    api = tradeapi.REST(key_id=headers['APCA-API-KEY-ID'],
                        secret_key=headers['APCA-API-SECRET-KEY'],
                        base_url=headers['APCA_API_BASE_URL'],
                        api_version='v2')

    db = sqlite3.connect('alpaca.db')
    db.row_factory = sqlite3.Row

    cursor = db.cursor()
    cursor.execute("SELECT id, symbol, company FROM stock")

    rows = cursor.fetchall()

    symbols=[]
    stock_dict={}
    for row in rows:
        symbol = row['symbol']
        symbols.append(symbol)
        stock_dict[symbol] = row['id']

    #print(symbols, stock_dict)
    chunk_size = 300
    for i in range(0,len(symbols),chunk_size):
        symbol_chunk = symbols[i:i+chunk_size]
        bars = api.get_bars(symbol_chunk,'1D',limit=100).df
        bars['ts'] = bars.index
        bars['date'] = bars['ts'].dt.date
        for symbol in bars['symbol']:
            for index, row in bars.iterrows():
                stock_id = stock_dict[row['symbol']]
                cursor.execute("""
                INSERT INTO stock_price (stock_id, date, open, high, low, close, volume)
                VALUES (?,?,?,?,?,?,?)
                """, (stock_id, row['date'], row['open'], row['high'], row['low'], row['close'], row['volume']))
    db.commit()

    # Check output
    from_db_pr = pd.read_sql(con=db, sql='SELECT * FROM stock_price')
    from_db_pr.to_csv("from_db_pr.csv")
    db.close()



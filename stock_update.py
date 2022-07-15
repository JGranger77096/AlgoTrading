# Step 4: update stock table programmatically

import sqlite3
import ssl_patch
import alpaca_trade_api as tradeapi
import json
import pandas as pd

headers = json.loads(open('Alpaca_Key.txt','r').read())

with ssl_patch.no_ssl_verification():
    api = tradeapi.REST(key_id=headers['APCA-API-KEY-ID'],
                        secret_key=headers['APCA-API-SECRET-KEY'],
                        base_url=headers['APCA_API_BASE_URL'],
                        api_version='v2')

    db = sqlite3.connect('alpaca.db')
    db.row_factory = sqlite3.Row

    cursor = db.cursor()
    cursor.execute("SELECT symbol, company FROM stock")

    rows = cursor.fetchall()
    symbols = [row['symbol'] for row in rows]

    assets = api.list_assets()

    for asset in assets:
        try:
            if asset.tradable and asset.symbol not in symbols:
                cursor.execute("INSERT INTO stock (symbol, company) VALUES(?,?)", (asset.symbol, asset.name))
        except Exception as e:
            print(asset.symbol)
            print(e)
    db.commit()
    db.close()

    # Check output
    db = sqlite3.connect('alpaca.db')
    from_db = pd.read_sql(con=db, sql='SELECT * FROM stock')
    from_db.to_csv("from_db.csv")
    db.close()

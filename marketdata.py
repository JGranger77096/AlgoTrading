import json, requests, sqlite3
import pandas as pd

headers = json.loads(open('Alpaca_Key.txt','r').read())
data_url = 'https://data.alpaca.markets/v2/stocks/bars/1Min?symbols='

#Specify the tickers
tickers = ['AAPL','AMZN','FB','GOOG','NFLX']
symbols = ",".join(tickers)
print(f'{data_url}{symbols}')
r = requests.get(f'{data_url}{symbols}', headers=headers, verify=False)
print(r.content)

#data = r.json()
#print(data)

#Establish database connection
db = sqlite3.connect("minutes.db")

#Define a create table function
def create_table(symbols):
    cursor = db.cursor()
    for symbol in symbols:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {symbol} (timestamp DATETIME PRIMARY KEY, open real(15,5), high REAL(15,5), low REAL(15,5), volume INTEGER)")
        try:
            db.commit()
        except:
            db.rollback()

#Create a table for each stock
create_table([ticker for ticker in tickers]) #list comprehension

#Load data into tables
for k,v in data.items():
    df = pd.DataFrame(data[k])
    df.columns = ['timestamp', 'open','high','low','close''volume']
    df['timestamp'] = pd.DatetimeIndex(pd.to_datetime(df['timestamp'], unit='s',).tz_localize('UTC').tz_convert('America/New_York'))
    df.to_sql(k, db, if_exists='append', index=False)

db.commit()
db.close()
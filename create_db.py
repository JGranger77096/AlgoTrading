# Step 3: create database of stock data
import sqlite3
import pandas as pd

# Establish database connection
db = sqlite3.connect("alpaca.db")

# Create a cursor
cursor = db.cursor()

# Create a stock table: Table 1
cursor.execute(""" CREATE TABLE IF NOT EXISTS stock (
               id INTEGER PRIMARY KEY,
               symbol TEXT NOT NULL UNIQUE,
               company TEXT NOT NULL UNIQUE
               )
               """)

# Create a stock table: Table 2
cursor.execute(""" CREATE TABLE IF NOT EXISTS stock_price (
               id INTEGER PRIMARY KEY,
               stock_id INTEGER,
               date NOT NULL,
               open NOT NULL,
               high NOT NULL,
               low NOT NULL,
               close NOT NULL,
               volume NOT NULL,
               FOREIGN KEY (stock_id) REFERENCES stock (id)
                )
                """)

db.commit()

# Check output
from_db = pd.read_sql(con=db,sql='SELECT * FROM stock_price')
from_db.to_csv("from_db_alp.csv")

db.close()
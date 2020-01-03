import bs4 as bs
import pickle #serializes any pytohn object
import requests
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import glob
from datetime import timedelta
import webscraping_2p500 as scrape

today = dt.datetime.today().date()
begin = today - timedelta(days=365)

print(today)
print(begin)

scrape.get__sp500_data_from_yahoo()
scrape.get__NASDAQ_data_from_yahoo()

print("DONE: Data Acquired ")
print("===========")

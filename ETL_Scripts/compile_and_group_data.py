import datetime as dt
import pandas as pd
from datetime import timedelta
import webscraping_2p500 as scrape
import glob

scrape.compile_data_long()

scrape.group_and_calculate()

print('DONE: Data Successfully Compiled and Grouped')
print('===========')
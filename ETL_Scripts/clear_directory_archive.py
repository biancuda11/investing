import shutil
import os
import datetime as dt
from datetime import datetime

source = 'C:/Users/us52873/Documents/Personal/investing/data_files/stock_dfs/'
dest1 = 'C:/Users/us52873/Documents/Personal/investing/data_files/archives/'

date = str(dt.datetime.today().date())

print('current date ', date)

files = os.listdir(source)

for f in files:
    ticker = f.split(".")[0]
    print(ticker)
    shutil.move(source+f, dest1 + ticker + date +'.csv')

print('DONE: Files moved')
print('===========')

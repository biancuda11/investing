import bs4 as bs
import pickle #serializes any pytohn object
import requests
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import glob
from datetime import timedelta

today = dt.datetime.today().date()
begin = today - timedelta(days=365)

print(today)
print(begin)

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker.replace('\n', '')
        tickers.append(ticker)

    with open("sp500_tickers.pickle", "wb") as f :
        pickle.dump(tickers, f)

    print(len(tickers))
    return tickers

# save_sp500_tickers()

def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500_tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = begin
    end = today

    bad_tickers = []

    for ticker in tickers:
        print(ticker + '\n')
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            try:
                df = web.DataReader(ticker , 'yahoo', start, end)
                df['50ma'] = df['Adj Close'].rolling(window=50, min_periods=0).mean()
                df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()
                df['200ma'] = df['Adj Close'].rolling(window=200, min_periods=0).mean()
                df['Symbol'] = ticker
                df.to_csv('stock_dfs/{}.csv'.format(ticker))
            except Exception as e:
                 print(f'Bad Ticker: {ticker}')
                 bad_tickers.append(ticker)

        else:
            print('Already have {}'.format(ticker))

# get_data_from_yahoo()

def compile_data_fat():
    with open("sp500_tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count,ticker in enumerate(tickers):
        try:
            df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
            df.set_index('Date', inplace=True)

            df.rename(columns = {'Adj Close': ticker}, inplace=True)
            df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

            if main_df.empty:
                main_df = df
            else:
                main_df = main_df.join(df, how='outer')

            if count % 10 == 0:
                print(count)

        except Exception as e:
            print('bad df')

    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')

def compile_data_long():
    path = 'C:/Users/us52873/Documents/Personal/investing/ETL_Scripts/stock_dfs'

    filenames= glob.glob(path+ "/*.csv")

    dfs = []

    for filename in filenames:
        df = pd.read_csv(filename)
        dfs.append(pd.read_csv(filename))

    frame = pd.concat(dfs, axis=0)

    print(frame.shape)

    frame.to_csv('final_df.csv', index=False, encoding='utf-8')

def group_and_calculate():

    df = pd.read_csv('C:/Users/us52873/Documents/Personal/investing/ETL_Scripts/final_df.csv')

    df = df.sort_values('Date').groupby('Symbol').tail(2)

    def above_100(row):

        if row['50ma'] > row['100ma']:
            return 'BUY'
        else:
            return 'SELL'

    df['Buy_Sell'] = df.apply(above_100,axis=1)

    df = df.sort_values(['Symbol', 'Date'], ascending=True)

    print(df)

    insert_index = 0

    for i, row in df.iterrows():

        symbol = row['Symbol']
        rating = row['Buy_Sell']

        if i == 0:
            continue
        else:
            if symbol == df.iloc[insert_index - 1, 10] and rating != df.iloc[insert_index - 1, 11]:
                print('Yahoo', row['Symbol'])

        insert_index += 1
        # same_symbol = row['Symbol'] == df.iloc[i-1]
        # changed_status = row['Buy_Sell'] != df.iloc[i-1, 1]

        # if same_symbol and not changed_status:
        #     print(row['Symbol'])


    df.to_csv('grouped_df.csv', index=False, encoding='utf-8')
#
# get_data_from_yahoo()
# print('============')
# compile_data_long()
# print('============')
group_and_calculate()
print('DONE')
print('============')
# compile_data_fat()
# save_sp500_tickers()
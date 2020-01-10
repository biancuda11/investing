import webscraping_2p500 as scrape

scrape.add_to_historical_file('detected_crosses_in_moving_avg', 'historical_moving_avg_cross')

scrape.add_to_historical_file('detected_price_thru_100day', 'historical_price_thru_100day')

print('DONE: Historical Changes Added')
print('===========')

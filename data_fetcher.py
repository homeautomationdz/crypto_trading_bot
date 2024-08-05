#file name data_fetcher.py

import pandas as pd
from binance.client import Client
import config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GetData:
    def __init__(self, symbol, timeframe='30m', limit=100):
        self.symbol = symbol
        self.timeframe = timeframe
        self.limit = limit
        self.df = self.fetch_binance_data()
        if not self.df.empty:
            self.df['timestamp'] = pd.to_datetime(self.df['timestamp'], unit='ms')
            self.df.set_index('timestamp', inplace=True)

    def fetch_binance_data(self):
        try:
            client = Client(config.api_key, config.api_secret)
            klines = client.get_historical_klines(self.symbol, self.timeframe, limit=self.limit)
            data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 
                                                'close_time', 'quote_asset_volume', 'number_of_trades', 
                                                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
            return data[['timestamp', 'open', 'high', 'low', 'close', 'volume', 
                          'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']]
        except Exception as e:
            logging.error(f"Error fetching data for {self.symbol}: {e}")
            return pd.DataFrame()
        

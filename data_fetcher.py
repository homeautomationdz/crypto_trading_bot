import pandas as pd
from binance.client import Client
import config3  # Adjust to your config file

def fetch_binance_data(symbol, timeframe='30m', limit=100):
    try:
        client = Client(config3.api_key, config3.api_secret)
        klines = client.get_historical_klines(symbol, timeframe, limit=limit)
        data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                             'close_time', 'quote_asset_volume', 'number_of_trades',
                                             'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        data['high'] = data['high'].astype(float)
        data['low'] = data['low'].astype(float)
        data['close'] = data['close'].astype(float)
        return data[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()

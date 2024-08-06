# tests/test_data_fetcher.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pandas as pd
from data_fetcher import GetData

def test_fetch_binance_data():
    data_fetcher = GetData('BTCUSDT')
    data = data_fetcher.fetch_binance_data()
    assert isinstance(data, pd.DataFrame)
    assert not data.empty

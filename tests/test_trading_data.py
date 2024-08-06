# tests/test_trading_data.py

import pandas as pd
import pytest
from trading_data import TradingData

def test_trading_data_metrics():
    data = pd.DataFrame({
        'open': [1, 2, 3],
        'close': [2, 3, 4],
        'high': [2, 3, 4],
        'low': [1, 2, 3],
        'taker_buy_base_asset_volume': [100, 200, 300],
        'taker_buy_quote_asset_volume': [150, 250, 350],
    }, index=pd.date_range(start='2024-01-01', periods=3, freq='H'))

    trading_data = TradingData(data)
    metrics = trading_data.calculate_metrics()

    assert metrics['current_price'] == 4
    assert metrics['buy_volume'] == 300
    assert metrics['sell_volume'] == 350

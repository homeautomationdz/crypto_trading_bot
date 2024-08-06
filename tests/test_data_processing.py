# tests/test_data_processing.py

import pandas as pd
import pytest
from data_processing import update_data, calculate_last_candle_volume, calculate_metrics

def test_update_data():
    # Create a sample DataFrame
    data = pd.DataFrame({
        'high': [1, 2, 3, 4, 5],
        'low': [0, 1, 2, 3, 4],
    }, index=pd.date_range(start='2024-01-01', periods=5, freq='H'))

    high, low = update_data(data)
    assert high == 5
    assert low == 0

def test_calculate_last_candle_volume():
    data = pd.DataFrame({
        'taker_buy_base_asset_volume': [100, 200],
        'taker_buy_quote_asset_volume': [150, 250],
    })

    buy_volume, sell_volume = calculate_last_candle_volume(data)
    assert buy_volume == 200
    assert sell_volume == 250

def test_calculate_metrics():
    data = pd.DataFrame({
        'open': [1, 2, 3],
        'close': [2, 3, 4],
        'high': [2, 3, 4],
        'low': [1, 2, 3],
        'taker_buy_base_asset_volume': [100, 200, 300],
        'taker_buy_quote_asset_volume': [150, 250, 350],
    }, index=pd.date_range(start='2024-01-01', periods=3, freq='H'))

    metrics = calculate_metrics(data)
    assert metrics['current_price'] == 4
    assert metrics['price_change'] == 33.33  # ((4 - 3) / 3) * 100

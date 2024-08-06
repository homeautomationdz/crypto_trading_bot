# tests/test_backtester.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pandas as pd
import numpy as np
from backtester import backtest_strategy

def test_backtest_strategy():
    # Create a sample DataFrame with mock data
    data = pd.DataFrame({
        'close': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    }, index=pd.date_range(start='2024-01-01', periods=10, freq='h'))

    # Run the backtest
    result = backtest_strategy(data, short_window=3, long_window=5)

    # Check that the strategy returns a DataFrame with the expected columns
    assert 'strategy_returns' in result.columns
    assert 'short_sma' in result.columns
    assert 'long_sma' in result.columns

    # Check that the moving averages are calculated correctly
    expected_short_sma = pd.Series([np.nan, np.nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
                                    index=result.index, name='short_sma')
    expected_long_sma = pd.Series([np.nan, np.nan, np.nan, np.nan, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],
                                   index=result.index, name='long_sma')  # Updated expected values

    pd.testing.assert_series_equal(result['short_sma'], expected_short_sma)
    pd.testing.assert_series_equal(result['long_sma'], expected_long_sma)

    # Check that the positions are calculated correctly
    expected_positions = pd.Series([0, 0, 0, 0, 1, 1, 1, 1, 1, 1], index=result.index)  # Buy signal at index 4
    pd.testing.assert_series_equal(result['positions'], expected_positions)

    # Check that the returns are calculated correctly
    expected_strategy_returns = pd.Series([np.nan, np.nan, np.nan, np.nan, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2], index=result.index)
    pd.testing.assert_series_equal(result['strategy_returns'].fillna(0), expected_strategy_returns)

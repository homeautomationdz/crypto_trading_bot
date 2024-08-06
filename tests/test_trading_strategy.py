import pandas as pd
import numpy as np

def backtest_strategy(data, short_window=3, long_window=5):
    """Backtest the trading strategy."""
    data['short_sma'] = data['close'].rolling(window=short_window).mean()
    data['long_sma'] = data['close'].rolling(window=long_window).mean()

    data['signal'] = 0
    data['signal'][short_window:] = np.where(data['short_sma'][short_window:] > data['long_sma'][short_window:], 1, 0)
    data['positions'] = data['signal'].diff()

    # Convert positions to integer type
    data['positions'] = data['positions'].fillna(0).astype(int)

    # Calculate returns
    data['returns'] = data['close'].pct_change()
    data['strategy_returns'] = data['returns'] * data['positions'].shift(1)

    return data
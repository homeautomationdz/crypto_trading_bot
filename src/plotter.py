# src/plotter.py
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_trendlines(df, peaks, troughs, breakout_indices, breakdown_indices, touching_indices, symbol, timeframe, high_timeframe, low_timeframe, buy_volume, sell_volume, volume_difference, price_change, timeframe_data):
    """
    Plot the closing price, trendlines, and high/low prices for specified timeframes.

    Args:
        df (pandas.DataFrame): The price data.
        peaks (list): List of peak points for trendlines.
        troughs (list): List of trough points for trendlines.
        breakout_indices (list): Indices of breakout points.
        breakdown_indices (list): Indices of breakdown points.
        touching_indices (list): Indices of touching points.
        symbol (str): The trading symbol.
        timeframe (str): The timeframe for the data.
        high_timeframe (float): The highest price in the specified timeframe.
        low_timeframe (float): The lowest price in the specified timeframe.
        buy_volume (float): The buy volume from the last candle.
        sell_volume (float): The sell volume from the last candle.
        volume_difference (float): The difference between buy and sell volume.
        price_change (float): The price change percentage.
        timeframe_data (dict): Dictionary containing high and low prices for multiple timeframes.
    """
    # Create the 'plots' directory if it doesn't exist
    plots_dir = 'plots'
    os.makedirs(plots_dir, exist_ok=True)

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['close'], label='Close Price', color='blue')

    # Plot high and low prices for each timeframe
    for timeframe, levels in timeframe_data.items():
        plt.axhline(y=levels['high'], color='green', linestyle='--', label=f'High {timeframe}')
        plt.axhline(y=levels['low'], color='red', linestyle='--', label=f'Low {timeframe}')

    # Plot trendlines if available
    if peaks is not None and len(peaks) > 0:
        peaks = [int(p) for p in peaks if isinstance(p, (int, np.integer))]  # Ensure peaks are integers
        plt.scatter(df.index[peaks], df['close'].iloc[peaks], color='orange', label='Peaks', marker='^', s=100)
    if troughs is not None and len(troughs) > 0:
        troughs = [int(t) for t in troughs if isinstance(t, (int, np.integer))]  # Ensure troughs are integers
        plt.scatter(df.index[troughs], df['close'].iloc[troughs], color='purple', label='Troughs', marker='v', s=100)

    # Highlight breakout and breakdown points
    if breakout_indices is not None and len(breakout_indices) > 0:
        breakout_indices = [int(b) for b in breakout_indices if isinstance(b, (int, np.integer))]  # Ensure breakout_indices are integers
        plt.scatter(df.index[breakout_indices], df['close'].iloc[breakout_indices], color='green', label='Breakouts', marker='o', s=100)
    if breakdown_indices is not None and len(breakdown_indices) > 0:
        breakdown_indices = [int(b) for b in breakdown_indices if isinstance(b, (int, np.integer))]  # Ensure breakdown_indices are integers
        plt.scatter(df.index[breakdown_indices], df['close'].iloc[breakdown_indices], color='red', label='Breakdowns', marker='x', s=100)

    plt.title(f'Trendlines and Price for {symbol} ({timeframe})')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.savefig(f'{plots_dir}/{symbol}_{timeframe}.png')
    plt.close()

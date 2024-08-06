import matplotlib.pyplot as plt
import io
import numpy as np
import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def plot_trendlines(data, trendline_peaks, trendline_troughs, breakout_indices, breakdown_indices, touching_indices, symbol, timeframe, high_30h, low_30h, buy_volume, sell_volume, volume_difference, price_change):
    """
    Plot trendlines, breakout and breakdown points, and various volume metrics.

    Args:
        data (pandas.DataFrame): The price data.
        trendline_peaks (numpy array): The calculated trendline peaks.
        trendline_troughs (numpy array): The calculated trendline troughs.
        breakout_indices (pandas.Index): Indices of breakout points.
        breakdown_indices (pandas.Index): Indices of breakdown points.
        touching_indices (pandas.Index): Indices of touching points.
        symbol (str): The trading symbol.
        timeframe (str): The timeframe for the data.
        high_30h (float): The highest price in the last 30 hours.
        low_30h (float): The lowest price in the last 30 hours.
        buy_volume (float): The buy volume from the last candle.
        sell_volume (float): The sell volume from the last candle.
        volume_difference (float): The difference between buy and sell volume.
        price_change (float): The price change percentage.

    Returns:
        BytesIO: A buffer containing the plot image.
    """
    try:
        plt.figure(figsize=(14, 7))

        # Plot closing price
        plt.plot(data.index, data['close'], label='Close Price', color='blue')

        # Create full arrays for trendlines
        trendline_peaks_full = np.full(data.shape[0], np.nan)
        trendline_troughs_full = np.full(data.shape[0], np.nan)

        # Fill in the trendlines where applicable
        trendline_peaks_full[-len(trendline_peaks):] = trendline_peaks
        trendline_troughs_full[-len(trendline_troughs):] = trendline_troughs

        # Plot trendlines
        plt.plot(data.index, trendline_peaks_full, label='Resistance Trendline', linestyle='--', color='red')
        plt.plot(data.index, trendline_troughs_full, label='Support Trendline', linestyle='--', color='green')

        # Plot breakout and breakdown points
        plt.scatter(data.loc[breakout_indices].index, data.loc[breakout_indices]['close'], color='blue', label='Breakout Points', marker='^')
        plt.scatter(data.loc[breakdown_indices].index, data.loc[breakdown_indices]['close'], color='orange', label='Breakdown Points', marker='v')
        plt.scatter(data.loc[touching_indices].index, data.loc[touching_indices]['close'], color='purple', label='Touch Points', marker='o')

        # Add volume metrics as text
        plt.text(data.index[-1], buy_volume, f'Buy Volume: {buy_volume}', color='green', fontsize=10, ha='right')
        plt.text(data.index[-1], sell_volume, f'Sell Volume: {sell_volume}', color='red', fontsize=10, ha='right')
        plt.text(data.index[-1], volume_difference, f'Volume Difference: {volume_difference}', color='gray', fontsize=10, ha='right')
        plt.text(data.index[-1], price_change, f'Price Change in 30 min: {price_change}%', color='purple', fontsize=10, ha='right')

        plt.xlabel('Timestamp')
        plt.ylabel('Price')
        plt.title(f'Trendline Breakout/Breakdown Detection for {symbol} ({timeframe})')
        plt.legend()
        plt.grid()
        
        # Save the plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)  # Move to the beginning of the BytesIO buffer
        plt.close()  # Close the figure to free up memory

        logging.info("Plot generated successfully.")
        return buf  # Return the buffer
    except Exception as e:
        logging.error(f"Error generating plot for {symbol}: {e}")
        logging.error(traceback.format_exc())
        return None  # Return None in case of an error

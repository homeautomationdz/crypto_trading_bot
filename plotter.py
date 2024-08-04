import matplotlib.pyplot as plt
import io

def plot_trendlines(data, trendline_peaks, trendline_troughs, breakout_indices, breakdown_indices, touching_indices, symbol, timeframe):
    plt.figure(figsize=(12, 6))
    plt.plot(data['timestamp'], data['close'], label='Close Price')
    plt.plot(data['timestamp'], trendline_peaks, label='Resistance Trendline', linestyle='--', color='red')
    plt.plot(data['timestamp'], trendline_troughs, label='Support Trendline', linestyle='--', color='green')
    plt.scatter(data.loc[breakout_indices]['timestamp'], data.loc[breakout_indices]['close'], color='blue', label='Breakout Points')
    plt.scatter(data.loc[breakdown_indices]['timestamp'], data.loc[breakdown_indices]['close'], color='orange', label='Breakdown Points')
    plt.scatter(data.loc[touching_indices]['timestamp'], data.loc[touching_indices]['close'], color='purple', label='Touch Points')
    plt.xlabel('Timestamp')
    plt.ylabel('Price')
    plt.legend()
    plt.title(f'Triangle Breakout/Breakdown Detection for {symbol} ({timeframe})')

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)  # Move to the beginning of the BytesIO buffer
    plt.close()  # Close the figure to free up memory
    return buf  # Return the buffer

import asyncio
from datetime import datetime, timezone
from data_fetcher import fetch_binance_data
from trendline_calculator import calculate_trendlines, detect_breakout_breakdown
from plotter import plot_trendlines
from telegram_notifier import send_image_to_telegram

# Global dictionary to store the last alert timestamp for each symbol
previous_alerts = {}
ALERT_COOLDOWN_HOURS = 1

async def check_for_breakouts_and_breakdowns(symbol, timeframe):
    data = fetch_binance_data(symbol, timeframe)
    if data.empty:
        print(f"No data fetched for {symbol}.")
        return

    trendline_peaks, trendline_troughs = calculate_trendlines(data)
    if trendline_peaks is None or trendline_troughs is None:
        print(f"Not enough data to calculate trendlines for {symbol}.")
        return

    breakout_indices, breakdown_indices, touching_indices = detect_breakout_breakdown(data, trendline_peaks, trendline_troughs)
    
    last_index = len(data) - 1
    now = datetime.now(timezone.utc)

    if (not breakout_indices.empty and breakout_indices[-1] == last_index) or \
       (not breakdown_indices.empty and breakdown_indices[-1] == last_index) or \
       (not touching_indices.empty and touching_indices[-1] == last_index):

        if symbol not in previous_alerts or (now - previous_alerts[symbol]).total_seconds() > ALERT_COOLDOWN_HOURS * 3600:
            previous_alerts[symbol] = now
            image_buffer = plot_trendlines(data, trendline_peaks, trendline_troughs, breakout_indices, breakdown_indices, touching_indices, symbol, timeframe)
            await send_image_to_telegram(image_buffer)

async def main():
    symbols = config3.SELECTED_SYMBOLS  # Use the selected symbols directly from config3.py
    timeframe = '30m'

    while True:
        print("Checking for breakouts and breakdowns...")
        tasks = [check_for_breakouts_and_breakdowns(symbol, timeframe) for symbol in symbols]
        await asyncio.gather(*tasks)
        print("Sleeping for 5 minutes...")
        await asyncio.sleep(300)  # Sleep for 5 minutes before checking again

if __name__ == "__main__":
    asyncio.run(main())

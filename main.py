import asyncio
from data_fetcher import GetData
from trendline_calculator import calculate_trendlines, detect_breakdowns
from plotter import plot_trendlines
from telegram_notifier import send_message_to_telegram, send_image_to_telegram
from trading_data import TradingData
import config

async def process_symbol(symbol):
    data_fetcher = GetData(symbol)
    trading_data = TradingData(data_fetcher.df)

    trendline_peaks, trendline_troughs = calculate_trendlines(data_fetcher.df)
    if trendline_peaks is None or trendline_troughs is None:
        print(f"Not enough data to calculate trendlines for {symbol}.")
        return

    breakout_indices, breakdown_indices, touching_indices = detect_breakdowns(data_fetcher.df, trendline_peaks, trendline_troughs)

    high_30h, low_30h = trading_data.update_data()
    buy_volume, sell_volume = trading_data.get_last_candle_volume()
    volume_difference = trading_data.calculate_volume_difference(buy_volume, sell_volume)
    price_change = trading_data.get_price_change()

    await send_message_to_telegram(symbol, high_30h, low_30h, buy_volume, sell_volume, volume_difference, price_change)

    image_buffer = plot_trendlines(data_fetcher.df, trendline_peaks, trendline_troughs, breakout_indices, breakdown_indices, touching_indices, symbol, data_fetcher.timeframe, high_30h, low_30h, buy_volume, sell_volume, volume_difference, price_change)
    await send_image_to_telegram(image_buffer)

async def main():
    symbols = config.SELECTED_SYMBOLS
    tasks = [process_symbol(symbol) for symbol in symbols]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

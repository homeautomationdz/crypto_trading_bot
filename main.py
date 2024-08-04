import asyncio
from telegram import Bot  # Import the Bot class
from data_fetcher import GetData
from trendline_calculator import calculate_trendlines, detect_breakdowns
from plotter import plot_trendlines
from telegram_notifier import send_message_to_telegram
from trading_data import TradingData
import config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def send_start_message():
    """Send a start message when the bot starts."""
    bot = Bot(token=config.bot_token)
    message = "Trading bot has started successfully!"
    try:
        await bot.send_message(chat_id=config.chat_id, text=message)
        logging.info("Start message sent to Telegram.")
    except Exception as e:
        logging.error(f"Error sending start message to Telegram: {e}")

async def process_symbol(symbol):
    logging.info(f"Processing symbol: {symbol}")
    data_fetcher = GetData(symbol)
    trading_data = TradingData(data_fetcher.df)

    trendline_peaks, trendline_troughs = calculate_trendlines(data_fetcher.df)
    if trendline_peaks is None or trendline_troughs is None:
        logging.warning(f"Not enough data to calculate trendlines for {symbol}.")
        return

    breakout_indices, breakdown_indices, touching_indices = detect_breakdowns(data_fetcher.df, trendline_peaks, trendline_troughs)

    high_30h, low_30h = trading_data.update_data()
    metrics = trading_data.calculate_metrics()

    if metrics is None:
        logging.warning(f"No metrics available for {symbol}.")
        return

    # Log metrics to the terminal
    logging.info(f"Metrics for {symbol}:")
    for key, value in metrics.items():
        logging.info(f" - {key.replace('_', ' ').title()}: {value:.2f}" if isinstance(value, float) else f" - {key.replace('_', ' ').title()}: {value}")

    # Check if price change is greater than 0.10%
    if metrics['price_change'] is not None and metrics['price_change'] > 0.10:
        # Generate the plot
        image_buffer = plot_trendlines(
            data_fetcher.df, trendline_peaks, trendline_troughs, breakout_indices, breakdown_indices,
            touching_indices, symbol, data_fetcher.timeframe, high_30h, low_30h,
            metrics['buy_volume'], metrics['sell_volume'], metrics['volume_difference'], metrics['price_change']
        )

        # Send metrics and plot to Telegram
        await send_message_to_telegram(
            symbol,
            metrics['current_price'],
            metrics['new_high'],
            metrics['new_low'],
            metrics['buy_volume'],
            metrics['sell_volume'],
            metrics['volume_difference'],
            metrics['volume_btc'],
            metrics['volume_percentage'],
            metrics['support'],
            metrics['resistance'],
            metrics['distance_from_support'],
            metrics['distance_from_resistance'],
            metrics['price_change'],
            image_buffer  # Pass the image buffer to the function
        )
    else:
        logging.info(f"No significant price change for {symbol}. Price change: {metrics['price_change']:.2f}%. No update sent to Telegram.")

async def main():
    # Send a start message
    await send_start_message()
    
    symbols = config.SELECTED_SYMBOLS
    for symbol in symbols:
        await process_symbol(symbol)  # Process each symbol one by one

if __name__ == "__main__":
    asyncio.run(main())

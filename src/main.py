# src/main.py
import asyncio
from telegram import Bot
from data_fetcher import GetData
from trendline_calculator import calculate_trendlines, detect_breakdowns
from plotter import plot_trendlines
from telegram_notifier import send_message_to_telegram
from trading_data import TradingData
from backtester import backtest_strategy
import config
import logging
import numpy as np
import traceback
from data_processing import update_data, update_data_multiple_timeframes  # Import update_data_multiple_timeframes

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
        logging.error(traceback.format_exc())

async def process_symbol(symbol, backtest=True):
    logging.info(f"Started processing symbol: {symbol}")
    try:
        data_fetcher = GetData(symbol)
        trading_data = TradingData(data_fetcher.df)

        if backtest:
            trading_data.data = backtest_strategy(trading_data.data, config.SHORT_WINDOW, config.LONG_WINDOW)
            logging.info(f"Backtesting results for {symbol}:\n{trading_data.data[['close', 'strategy_returns']].tail()}")
            logging.info(f"Backtesting completed for {symbol}.")
            return

        # Apply the trading strategy
        trading_data.apply_strategy(config.SHORT_WINDOW, config.LONG_WINDOW)

        # Log the last few rows of data to see signals
        logging.info(f"Last few rows with signals for {symbol}:\n{trading_data.data.tail()}")

        try:
            trendline_peaks, trendline_troughs = calculate_trendlines(data_fetcher.df)
            if trendline_peaks is None or trendline_troughs is None:
                logging.warning(f"Not enough data to calculate trendlines for {symbol}.")
                return
        except Exception as e:
            logging.error(f"Error calculating trendlines for {symbol}: {e}")
            logging.error(traceback.format_exc())
            return

        breakout_indices, breakdown_indices, touching_indices = detect_breakdowns(data_fetcher.df, trendline_peaks, trendline_troughs)

        # Get high and low prices for multiple timeframes
        timeframe_data = update_data_multiple_timeframes(data_fetcher.df)
        high_timeframe, low_timeframe = update_data(data_fetcher.df)
        
        # Ensure high_timeframe and low_timeframe are floats
        high_timeframe = float(high_timeframe)
        low_timeframe = float(low_timeframe)

        metrics = trading_data.calculate_metrics()

        if metrics is None:
            logging.warning(f"No metrics available for {symbol}.")
            return

        # Check proximity to high and low prices
        current_price = metrics['current_price']
        proximity_alert = ""
        
        # Check proximity to support and resistance levels
        if abs(current_price - low_timeframe) / low_timeframe <= 0.05:  # Within 5% of support
            proximity_alert = "🟢"
        elif abs(current_price - high_timeframe) / high_timeframe <= 0.05:  # Within 5% of resistance
            proximity_alert = "🔴"

        # Log metrics to the terminal
        logging.info(f"Metrics for {symbol}:")
        for key, value in metrics.items():
            logging.info(f" - {key.replace('_', ' ').title()}: {value:.2f}" if isinstance(value, float) else f" - {key.replace('_', ' ').title()}: {value}")

        # Check if price change is greater than 0.10%
        if metrics['price_change'] is not None and metrics['price_change'] > 0.10:
            # Generate the plot
            image_buffer = plot_trendlines(
                data_fetcher.df, trendline_peaks, trendline_troughs, breakout_indices, breakdown_indices,
                touching_indices, symbol, data_fetcher.timeframe, high_timeframe, low_timeframe,
                metrics['buy_volume'], metrics['sell_volume'], metrics['volume_difference'], metrics['price_change'],
                timeframe_data  # Pass the timeframe data for plotting
            )

            # Send metrics and plot to Telegram
            logging.info(f"Sending Telegram notification for {symbol}.")
            await send_message_to_telegram(
                symbol + proximity_alert,  # Append proximity alert to symbol
                metrics['current_price'],
                high_timeframe,  # Ensure these are floats
                low_timeframe,    # Ensure these are floats
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
                image_buffer  # Pass the image buffer if you have one
            )
        else:
            logging.info(f"No significant price change for {symbol}. Price change: {metrics['price_change']:.2f}%. No update sent to Telegram.")
    except Exception as e:
        logging.error(f"Error processing symbol {symbol}: {e}")
        logging.error(traceback.format_exc())

async def main():
    # Send a start message
    await send_start_message()
    
    symbols = config.SELECTED_SYMBOLS
    for symbol in symbols:
        await process_symbol(symbol, backtest=False)  # Process each symbol one by one

if __name__ == "__main__":
    asyncio.run(main())

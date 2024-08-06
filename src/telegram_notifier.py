# src/telegram_notifier.py
from telegram import Bot
import logging
import config  # Ensure you import the config module
import pandas as pd  # Import pandas for date formatting
async def send_message_to_telegram(symbol, current_price, high_timeframe, low_timeframe, buy_volume, sell_volume, volume_difference, volume_btc, volume_percentage, support, resistance, distance_from_support, distance_from_resistance, price_change, image_buffer):
    """
    Send a message to Telegram with trading metrics and a plot image.

    Args:
        symbol (str): The trading symbol.
        current_price (float): The current price of the asset.
        high_timeframe (float): The highest price in the specified timeframe.
        low_timeframe (float): The lowest price in the specified timeframe.
        buy_volume (float): The buy volume from the last candle.
        sell_volume (float): The sell volume from the last candle.
        volume_difference (float): The difference between buy and sell volume.
        volume_btc (float): The volume in BTC.
        volume_percentage (float): The volume percentage.
        support (float): The support level.
        resistance (float): The resistance level.
        distance_from_support (float): Distance from support in percentage.
        distance_from_resistance (float): Distance from resistance in percentage.
        price_change (float): The price change percentage.
        image_buffer (BytesIO): The plot image buffer.
    """
    bot = Bot(token=config.bot_token)
    
    # Constructing the notification message
    message = (
        f"📊 Trading Update for {symbol} ({config.TIMEFRAME})\n"
        f"📈 Current Price: {current_price:.4f}\n"
        f"📈 Highest Price ({config.TIMEFRAME}): {high_timeframe:.4f}\n"
        f"📉 Lowest Price ({config.TIMEFRAME}): {low_timeframe:.4f}\n"
        f"🔼 Last Candle Buy Volume: {buy_volume:.2f}\n"
        f"🔽 Last Candle Sell Volume: {sell_volume:.2f}\n"
        f"📊 Volume Difference: {volume_difference:.2f}\n"
        f"💰 Volume in BTC: {volume_btc:.2f}\n"
        f"📈 Volume Percentage: {volume_percentage:.2f}%\n"
        f"📉 Support Level: {support:.4f}\n"
        f"📈 Resistance Level: {resistance:.4f}\n"
        f"📏 Distance from Support: {distance_from_support:.2f}%\n"
        f"📏 Distance from Resistance: {distance_from_resistance:.2f}%\n"
        f"📉 Price Change: {price_change:.2f}%\n"
        f"Time: {pd.Timestamp.now().strftime('%d-%m-%Y %I:%M:%S %p')}\n"
        f"𝙏𝙑 Trading View Chart (Click here) (https://www.tradingview.com/chart?symbol=Binance%3A{symbol}USDT&interval={config.TIMEFRAME})"
    )

    try:
        await bot.send_message(chat_id=config.chat_id, text=message)
        if image_buffer:
            await bot.send_photo(chat_id=config.chat_id, photo=image_buffer)
        logging.info(f"Notification sent for {symbol}.")
    except Exception as e:
        logging.error(f"Error sending Telegram message for {symbol}: {e}")

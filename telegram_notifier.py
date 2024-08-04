from telegram import Bot
from telegram.error import TelegramError
import config
import logging
import asyncio

async def send_message_to_telegram(symbol, current_price, new_high, new_low, buy_volume, sell_volume, volume_difference, volume_btc, volume_percentage, support, resistance, distance_from_support, distance_from_resistance, price_change, image_buffer=None):
    bot = Bot(token=config.bot_token)
    try:
        message = f"Symbol: {symbol}\n"
        message += f"New 30-hour High: {new_high}\n"
        message += f"New 30-hour Low: {new_low}\n"
        message += f"Last Candle 30 min Buy Volume: {buy_volume}\n"
        message += f"Last Candle 30 min Sell Volume: {sell_volume}\n"
        message += f"Volume Difference: {volume_difference}\n"
        message += f"Price Change in 30 min: {price_change}%\n"

        # Send the message
        await bot.send_message(chat_id=config.chat_id, text=message)

        # If an image buffer is provided, send the plot
        if image_buffer:
            await bot.send_photo(chat_id=config.chat_id, photo=image_buffer)
            logging.info(f"Plot sent to Telegram for symbol {symbol}")

    except TelegramError as e:
        logging.error(f"Error sending message to Telegram for symbol {symbol}: {e}")

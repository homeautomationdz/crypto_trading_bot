from telegram import Bot
from telegram.error import TelegramError
import config

async def send_message_to_telegram(symbol, high_30h, low_30h, buy_volume, sell_volume, volume_difference, price_change):
    bot = Bot(token=config.bot_token)
    try:
        message = f"Symbol: {symbol}\n"
        message += f"New 30-hour High: {high_30h}\n"
        message += f"New 30-hour Low: {low_30h}\n"
        message += f"Last Candle 30 min Buy Volume: {buy_volume}\n"
        message += f"Last Candle 30 min Sell Volume: {sell_volume}\n"
        message += f"Volume Difference: {volume_difference}\n"
        message += f"Price Change in 30 min: {price_change}%\n"
        await bot.send_message(chat_id=config.chat_id, text=message)
    except TelegramError as e:
        print(f"Error sending message to Telegram: {e}")

async def send_image_to_telegram(image_buffer):
    bot = Bot(token=config.bot_token)
    try:
        await bot.send_photo(chat_id=config.chat_id, photo=image_buffer)
    except TelegramError as e:
        print(f"Error sending image to Telegram: {e}")

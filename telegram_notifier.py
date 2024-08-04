from telegram import Bot
from telegram.error import TelegramError
import config3  # Adjust to your config file

async def send_image_to_telegram(image_buffer):
    bot = Bot(token=config3.bot_token)  # Use the bot token from config3.py
    try:
        await bot.send_photo(chat_id=config3.chat_id, photo=image_buffer)  # Send the image buffer directly
    except TelegramError as e:
        print(f"Error sending image to Telegram: {e}")

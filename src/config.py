from dotenv import load_dotenv
import os
import logging

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Fetching API credentials and bot token from environment variables
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
bot_token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHAT_ID')

# Check if essential environment variables are set
if not api_key or not api_secret or not bot_token or not chat_id:
    logging.error("One or more environment variables are not set. Please check your .env file.")
    raise ValueError("Missing required environment variables.")

# Selected trading symbols (without 'USDT')
SELECTED_SYMBOLS = [
    'AAVEUSDT', 'ACEUSDT', 'ACHUSDT', 'ADAUSDT', 'AEVOUSDT', 'AGLDUSDT', 
    'ALGOUSDT', 'ALICEUSDT', 'ALPHAUSDT', 'ALTUSDT', 'AMBUSDT', 'APTUSDT',
    'ARBUSDT', 'ARKUSDT', 'ARPAUSDT', 'ARUSDT', 'ASTRUSDT', 'ATAUSDT', 
    'ATOMUSDT', 'AUCTIONUSDT', 'AVAXUSDT', 'AXLUSDT', 'AXSUSDT', 
    'BADGERUSDT', 'BAKEUSDT', 'BALUSDT', 'BANDUSDT', 'BATUSDT', 'BBUSDT'
]

# Trading strategy parameters
SHORT_WINDOW = 5  # Short-term moving average window
LONG_WINDOW = 20   # Long-term moving average window

# Timeframe for data fetching
TIMEFRAME = '1h'  # Default timeframe (can be changed to '1m', '5m', '1h', '1d', etc.)

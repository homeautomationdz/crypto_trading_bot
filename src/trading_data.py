import pandas as pd
import logging
from data_processing import update_data, calculate_last_candle_volume, calculate_metrics, generate_signals
import numpy as np
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TradingData:
    def __init__(self, data):
        """
        Initialize the TradingData object with price data.
        
        Args:
            data (pandas.DataFrame): The price data.
        """
        self.data = data

    def update_data(self):
        """Update data to get the highest and lowest prices in the last specified timeframe."""
        try:
            logging.info("Updating data to get highest and lowest prices in the last specified timeframe.")
            return update_data(self.data)
        except Exception as e:
            logging.error(f"Error updating data: {e}")
            logging.error(traceback.format_exc())
            return None, None

    def get_last_candle_volume(self):
        """Get the buy and sell volume from the last candle."""
        try:
            logging.info("Calculating buy and sell volume from the last candle.")
            return calculate_last_candle_volume(self.data)
        except Exception as e:
            logging.error(f"Error getting last candle volume: {e}")
            logging.error(traceback.format_exc())
            return 0.0, 0.0

    def calculate_metrics(self):
        """Calculate various trading metrics."""
        try:
            logging.info("Calculating trading metrics.")
            return calculate_metrics(self.data)
        except Exception as e:
            logging.error(f"Error calculating metrics: {e}")
            logging.error(traceback.format_exc())
            return None

    def apply_strategy(self, short_window=5, long_window=20):
        """Apply trading strategy to the data."""
        try:
            logging.info("Applying trading strategy to the data.")
            self.data = generate_signals(self.data, short_window, long_window)
            
            # Log buy/sell signals
            for index, row in self.data.iterrows():
                if row['positions'] == 1:
                    logging.info(f"Buy signal generated at {index}: Price: {row['close']}")
                elif row['positions'] == -1:
                    logging.info(f"Sell signal generated at {index}: Price: {row['close']}")
            
            logging.info("Trading strategy applied successfully.")
            return self.data
        except Exception as e:
            logging.error(f"Error applying trading strategy: {e}")
            logging.error(traceback.format_exc())
            return self.data

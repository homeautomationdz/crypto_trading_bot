# src/data_processing.py
import pandas as pd
import logging
import numpy as np
import traceback
import config  # Import the config to access TIMEFRAME

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update_data(data):
    """
    Update data to get the highest and lowest prices in the specified timeframe.
    
    Args:
        data (pandas.DataFrame): The price data.
    
    Returns:
        tuple: A tuple containing the highest price (float) and lowest price (float) in the specified timeframe.
    """
    try:
        logging.info(f"Updating data to get highest and lowest prices in the last {config.TIMEFRAME}.")
        
        # Convert the TIMEFRAME to a Timedelta
        if config.TIMEFRAME.endswith('h'):
            hours = int(config.TIMEFRAME[:-1])
            time_delta = pd.Timedelta(hours=hours)
        elif config.TIMEFRAME.endswith('m'):
            minutes = int(config.TIMEFRAME[:-1])
            time_delta = pd.Timedelta(minutes=minutes)
        else:
            logging.error("Invalid timeframe format. Please use '1h', '30m', etc.")
            return None, None
        
        timeframe_ago = data.index[-1] - time_delta
        recent_data = data[data.index >= timeframe_ago]

        if not recent_data.empty:
            high_timeframe = recent_data["high"].max()
            low_timeframe = recent_data["low"].min()
            logging.info(f"Highest price in the last {config.TIMEFRAME}: {high_timeframe}")
            logging.info(f"Lowest price in the last {config.TIMEFRAME}: {low_timeframe}")
            return high_timeframe, low_timeframe
        else:
            logging.warning("No recent data available to update prices.")
            return None, None
    except Exception as e:
        logging.error(f"Error updating data: {e}")
        logging.error(traceback.format_exc())
        return None, None

def update_data_multiple_timeframes(data):
    """
    Update data to get the highest and lowest prices for multiple timeframes.
    
    Args:
        data (pandas.DataFrame): The price data.
    
    Returns:
        dict: A dictionary containing high and low prices for specified timeframes.
    """
    timeframes = ['30m', '1h', '4h', '1d']
    results = {}
    
    for timeframe in timeframes:
        try:
            if timeframe.endswith('h'):
                hours = int(timeframe[:-1])
                time_delta = pd.Timedelta(hours=hours)
            elif timeframe.endswith('m'):
                minutes = int(timeframe[:-1])
                time_delta = pd.Timedelta(minutes=minutes)
            else:
                continue
            
            timeframe_ago = data.index[-1] - time_delta
            recent_data = data[data.index >= timeframe_ago]

            if not recent_data.empty:
                high = recent_data["high"].max()
                low = recent_data["low"].min()
                results[timeframe] = {'high': high, 'low': low}
                logging.info(f"Highest price in the last {timeframe}: {high}")
                logging.info(f"Lowest price in the last {timeframe}: {low}")
        except Exception as e:
            logging.error(f"Error updating data for timeframe {timeframe}: {e}")
    
    return results

def calculate_last_candle_volume(data):
    """
    Get the buy and sell volume from the last candle.
    
    Args:
        data (pandas.DataFrame): The price data.
    
    Returns:
        tuple: A tuple containing the buy volume (float) and sell volume (float).
    """
    try:
        if not data.empty:
            last_candle = data.iloc[-1]
            buy_volume = pd.to_numeric(last_candle["taker_buy_base_asset_volume"], errors='coerce')
            sell_volume = pd.to_numeric(last_candle["taker_buy_quote_asset_volume"], errors='coerce')
            return buy_volume if not pd.isna(buy_volume) else 0.0, sell_volume if not pd.isna(sell_volume) else 0.0
        return 0.0, 0.0
    except Exception as e:
        logging.error(f"Error calculating last candle volume: {e}")
        logging.error(traceback.format_exc())
        return 0.0, 0.0

def calculate_metrics(data):
    """
    Calculate various trading metrics.
    
    Args:
        data (pandas.DataFrame): The price data.
    
    Returns:
        dict or None: A dictionary containing the calculated metrics, or None if an error occurs.
    """
    try:
        logging.info("Calculating trading metrics.")
        if data.empty:
            logging.warning("No data available for calculating metrics.")
            return None

        current_price = pd.to_numeric(data['close'].iloc[-1], errors='coerce')
        high_timeframe, low_timeframe = update_data(data)
        buy_volume, sell_volume = calculate_last_candle_volume(data)
        volume_difference = buy_volume - sell_volume

        # Calculate volume in BTC
        volume_btc = buy_volume * current_price  # Assuming buy_volume is in base asset
        volume_percentage = (volume_btc / (buy_volume + sell_volume)) * 100 if (buy_volume + sell_volume) > 0 else 0

        # Support and Resistance levels
        support = pd.to_numeric(low_timeframe, errors='coerce')
        resistance = pd.to_numeric(high_timeframe, errors='coerce')
        distance_from_support = ((current_price - support) / support) * 100 if support > 0 else None
        distance_from_resistance = ((current_price - resistance) / resistance) * 100 if resistance > 0 else None

        metrics = {
            'current_price': current_price,
            'high_timeframe': high_timeframe,
            'low_timeframe': low_timeframe,
            'buy_volume': buy_volume,
            'sell_volume': sell_volume,
            'volume_difference': volume_difference,
            'volume_btc': volume_btc,
            'volume_percentage': volume_percentage,
            'support': support,
            'resistance': resistance,
            'distance_from_support': distance_from_support,
            'distance_from_resistance': distance_from_resistance,
            'price_change': get_price_change(data)
        }

        logging.info("Trading metrics calculated successfully.")
        return metrics
    except Exception as e:
        logging.error(f"Error calculating metrics: {e}")
        logging.error(traceback.format_exc())
        return None

def get_price_change(data):
    """
    Calculate the price change percentage.
    
    Args:
        data (pandas.DataFrame): The price data.
    
    Returns:
        float or None: The price change percentage, or None if an error occurs.
    """
    try:
        if not data.empty:
            open_price = pd.to_numeric(data['open'].iloc[-1], errors='coerce')
            close_price = pd.to_numeric(data['close'].iloc[-1], errors='coerce')
            if pd.isna(open_price) or pd.isna(close_price):
                return None
            return round((close_price - open_price) / open_price * 100, 2)
        return None
    except Exception as e:
        logging.error(f"Error calculating price change: {e}")
        logging.error(traceback.format_exc())
        return None

def calculate_sma(data, window):
    """
    Calculate Simple Moving Average (SMA).
    
    Args:
        data (pandas.DataFrame): The price data.
        window (int): The window size for the SMA.
    
    Returns:
        pandas.Series: The calculated SMA.
    """
    try:
        return data['close'].rolling(window=window).mean()
    except Exception as e:
        logging.error(f"Error calculating SMA: {e}")
        logging.error(traceback.format_exc())
        return None

def generate_signals(data, short_window=5, long_window=20):
    """
    Generate buy/sell signals based on SMA crossover.
    
    Args:
        data (pandas.DataFrame): The price data.
        short_window (int): The short-term moving average window.
        long_window (int): The long-term moving average window.
    
    Returns:
        pandas.DataFrame: The data with signals added.
    """
    try:
        logging.info("Generating buy/sell signals based on SMA crossover.")
        data['short_sma'] = calculate_sma(data, short_window)
        data['long_sma'] = calculate_sma(data, long_window)

        # Create signals using .loc
        data['signal'] = 0
        data.loc[data.index[short_window:], 'signal'] = np.where(data['short_sma'][short_window:] > data['long_sma'][short_window:], 1, 0)
        data['positions'] = data['signal'].diff()

        logging.info("Signals generated successfully.")
        return data
    except Exception as e:
        logging.error(f"Error generating signals: {e}")
        logging.error(traceback.format_exc())
        return data

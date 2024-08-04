import pandas as pd
import logging

class TradingData:
    def __init__(self, data):
        self.data = data

    def update_data(self):
        thirty_hours_ago = self.data.index[-1] - pd.Timedelta(hours=30)
        recent_data = self.data[self.data.index >= thirty_hours_ago]

        if not recent_data.empty:
            high_30h = recent_data["high"].max()
            low_30h = recent_data["low"].min()
        else:
            high_30h = None
            low_30h = None

        return high_30h, low_30h

    def get_last_candle_volume(self):
        if not self.data.empty:
            last_candle = self.data.iloc[-1]
            buy_volume = pd.to_numeric(last_candle["taker_buy_base_asset_volume"], errors='coerce')
            sell_volume = pd.to_numeric(last_candle["taker_buy_quote_asset_volume"], errors='coerce')
            return buy_volume if not pd.isna(buy_volume) else 0.0, sell_volume if not pd.isna(sell_volume) else 0.0
        return 0.0, 0.0

    def calculate_volume_difference(self, buy_volume, sell_volume):
        return buy_volume - sell_volume

    def get_price_change(self):
        if not self.data.empty:
            open_price = pd.to_numeric(self.data['open'].iloc[-1], errors='coerce')
            close_price = pd.to_numeric(self.data['close'].iloc[-1], errors='coerce')
            if pd.isna(open_price) or pd.isna(close_price):
                return None
            return round((close_price - open_price) / open_price * 100, 2)
        return None

    def calculate_metrics(self):
        """Calculate additional metrics for the trading data."""
        if self.data.empty:
            logging.warning("No data available for calculating metrics.")
            return None

        current_price = pd.to_numeric(self.data['close'].iloc[-1], errors='coerce')
        new_high = pd.to_numeric(self.data['high'].max(), errors='coerce')
        new_low = pd.to_numeric(self.data['low'].min(), errors='coerce')
        buy_volume, sell_volume = self.get_last_candle_volume()
        volume_difference = self.calculate_volume_difference(buy_volume, sell_volume)

        # Calculate volume in BTC
        volume_btc = buy_volume * current_price  # Assuming buy_volume is in base asset
        volume_percentage = (volume_btc / (buy_volume + sell_volume)) * 100 if (buy_volume + sell_volume) > 0 else 0

        # Support and Resistance levels
        support = new_low
        resistance = new_high
        distance_from_support = ((current_price - support) / support) * 100 if support > 0 else None
        distance_from_resistance = ((current_price - resistance) / resistance) * 100 if resistance > 0 else None

        metrics = {
            'current_price': current_price,
            'new_high': new_high,
            'new_low': new_low,
            'buy_volume': buy_volume,
            'sell_volume': sell_volume,
            'volume_difference': volume_difference,
            'volume_btc': volume_btc,
            'volume_percentage': volume_percentage,
            'support': support,
            'resistance': resistance,
            'distance_from_support': distance_from_support,
            'distance_from_resistance': distance_from_resistance,
            'price_change': self.get_price_change()
        }

        # Log metrics to the terminal
        logging.info(f"Metrics for {self.data.index[-1]}:")
        for key, value in metrics.items():
            logging.info(f" - {key.replace('_', ' ').title()}: {value:.2f}" if isinstance(value, float) else f" - {key.replace('_', ' ').title()}: {value}")

        return metrics

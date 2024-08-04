import pandas as pd

class TradingData:
    def __init__(self, data):
        self.data = data

    def update_data(self):
        # Calculate the high and low for the last 30 hours (1800 minutes)
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
            # Use pd.to_numeric to ensure conversion and handle errors
            buy_volume = pd.to_numeric(last_candle["taker_buy_base_asset_volume"], errors='coerce')
            sell_volume = pd.to_numeric(last_candle["taker_buy_quote_asset_volume"], errors='coerce')
            # If conversion results in NaN, set to 0
            return buy_volume if not pd.isna(buy_volume) else 0.0, sell_volume if not pd.isna(sell_volume) else 0.0
        return 0.0, 0.0

    def calculate_volume_difference(self, buy_volume, sell_volume):
        return buy_volume - sell_volume

    def get_price_change(self):
        if not self.data.empty:
            # Convert values to numeric types
            open_price = pd.to_numeric(self.data['open'].iloc[-1], errors='coerce')
            close_price = pd.to_numeric(self.data['close'].iloc[-1], errors='coerce')
            if pd.isna(open_price) or pd.isna(close_price):
                return None  # Handle case where conversion fails
            return round((close_price - open_price) / open_price * 100, 2)
        return None

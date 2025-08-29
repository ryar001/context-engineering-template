import pandas as pd
import pandas_ta as ta # type: ignore
from decimal import Decimal

class TechnicalAnalyzer:
    def __init__(self):
        self.data = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'volume', 'timestamp'])
        self.data = self.data.set_index('timestamp') # Set timestamp as index

    def add_ohlcv_data(self, ochlv_data):
        # Convert Decimal to float for pandas_ta calculations
        new_row = pd.DataFrame([{
            'open': float(ochlv_data.open),
            'high': float(ochlv_data.high),
            'low': float(ochlv_data.low),
            'close': float(ochlv_data.close),
            'volume': float(ochlv_data.volume)
        }], index=[ochlv_data.timestamp])
        self.data = pd.concat([self.data, new_row])
        # Keep only the last N data points to avoid excessive memory usage
        self.data = self.data.iloc[-200:] # Keep last 200 data points for indicators

    def calculate_rsi(self, length=14):
        if len(self.data) < length:
            return None
        return ta.rsi(self.data["close"], length=length).iloc[-1]

    def calculate_macd(self, fast=12, slow=26, signal=9):
        if len(self.data) < max(fast, slow, signal):
            return None, None, None
        macd = ta.macd(self.data["close"], fast=fast, slow=slow, signal=signal)
        return macd["MACD"].iloc[-1], macd["MACDH"].iloc[-1], macd["MACDS"].iloc[-1]

    def calculate_sma(self, length=20):
        if len(self.data) < length:
            return None
        return ta.sma(self.data["close"], length=length).iloc[-1]

    def calculate_ema(self, length=20):
        if len(self.data) < length:
            return None
        return ta.ema(self.data["close"], length=length).iloc[-1]

    def get_latest_data(self):
        if self.data.empty:
            return None
        latest_row = self.data.iloc[-1]
        return {
            "open": Decimal(str(latest_row["open"])),
            "high": Decimal(str(latest_row["high"])),
            "low": Decimal(str(latest_row["low"])),
            "close": Decimal(str(latest_row["close"])),
            "volume": Decimal(str(latest_row["volume"])),
            "timestamp": self.data.index[-1]
        }
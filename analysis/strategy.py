from analysis.technical_analyzer import TechnicalAnalyzer
from models import OCHLVData, TradeSignal
from decimal import Decimal

class TradingStrategy:
    def __init__(self, technical_analyzer: TechnicalAnalyzer):
        self.technical_analyzer = technical_analyzer

    def generate_signal(self, ochlv_data: OCHLVData) -> TradeSignal | None:
        self.technical_analyzer.add_ohlcv_data(ochlv_data)

        # Simple strategy: Buy if RSI is below 30 (oversold) and MACD crosses up
        # Sell if RSI is above 70 (overbought) and MACD crosses down

        rsi = self.technical_analyzer.calculate_rsi()
        macd, macdh, macds = self.technical_analyzer.calculate_macd()
        latest_close = ochlv_data.close

        if rsi is None or macd is None or macdh is None or macds is None:
            return None

        # Entry condition (Buy)
        if rsi < 30 and macdh > 0 and macdh > macds: # MACD Histogram positive and MACD line crosses above signal line
            # For simplicity, setting stop loss and take profit as fixed percentages
            # In a real scenario, these would be dynamically calculated based on ATR, support/resistance, etc.
            stop_loss = latest_close * Decimal('0.99') # 1% below
            take_profit = latest_close * Decimal('1.02') # 2% above
            return TradeSignal(action='enter', stop_loss=stop_loss, take_profit=take_profit)

        # Exit condition (Sell) - This strategy assumes we are already in a trade
        # A more robust strategy would manage open positions
        if rsi > 70 and macdh < 0 and macdh < macds: # MACD Histogram negative and MACD line crosses below signal line
            return TradeSignal(action='exit')

        return None
import unittest
from unittest.mock import MagicMock
from decimal import Decimal
from analysis.strategy import TradingStrategy
from models import OCHLVData, TradeSignal

class TestTradingStrategy(unittest.TestCase):

    def setUp(self):
        self.mock_technical_analyzer = MagicMock()
        self.strategy = TradingStrategy(self.mock_technical_analyzer)
        self.sample_ochlv_data = OCHLVData(
            timestamp=1234567890,
            open=Decimal('100.00'),
            high=Decimal('105.00'),
            low=Decimal('98.00'),
            close=Decimal('102.00'),
            volume=Decimal('1000.00')
        )

    def test_generate_signal_no_signal(self):
        self.mock_technical_analyzer.calculate_rsi.return_value = 50
        self.mock_technical_analyzer.calculate_macd.return_value = (0.5, 0.1, 0.4) # MACD, MACDH, MACDS
        signal = self.strategy.generate_signal(self.sample_ochlv_data)
        self.assertIsNone(signal)
        self.mock_technical_analyzer.add_ohlcv_data.assert_called_once_with(self.sample_ochlv_data)

    def test_generate_signal_enter_condition(self):
        self.mock_technical_analyzer.calculate_rsi.return_value = 25 # Oversold
        self.mock_technical_analyzer.calculate_macd.return_value = (0.5, 0.1, 0.05) # MACDH positive, MACD > MACDS
        signal = self.strategy.generate_signal(self.sample_ochlv_data)
        self.assertIsInstance(signal, TradeSignal)
        self.assertEqual(signal.action, 'enter')
        self.assertIsNotNone(signal.stop_loss)
        self.assertIsNotNone(signal.take_profit)
        self.assertEqual(signal.stop_loss, self.sample_ochlv_data.close * Decimal('0.99'))
        self.assertEqual(signal.take_profit, self.sample_ochlv_data.close * Decimal('1.02'))

    def test_generate_signal_exit_condition(self):
        self.mock_technical_analyzer.calculate_rsi.return_value = 75 # Overbought
        self.mock_technical_analyzer.calculate_macd.return_value = (-0.5, -0.1, -0.05) # MACDH negative, MACD < MACDS
        signal = self.strategy.generate_signal(self.sample_ochlv_data)
        self.assertIsInstance(signal, TradeSignal)
        self.assertEqual(signal.action, 'exit')
        self.assertIsNone(signal.stop_loss)
        self.assertIsNone(signal.take_profit)

    def test_generate_signal_insufficient_data(self):
        self.mock_technical_analyzer.calculate_rsi.return_value = None
        self.mock_technical_analyzer.calculate_macd.return_value = (None, None, None)
        signal = self.strategy.generate_signal(self.sample_ochlv_data)
        self.assertIsNone(signal)

if __name__ == '__main__':
    unittest.main()
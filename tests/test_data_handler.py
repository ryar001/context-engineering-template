import unittest
from unittest.mock import MagicMock, patch
import json
from decimal import Decimal
from data.data_handler import DataHandler
from models import OCHLVData

class TestDataHandler(unittest.TestCase):

    def setUp(self):
        self.symbol = "BTCUSDT"
        self.interval = "1m"
        self.mock_callback = MagicMock()
        self.data_handler = DataHandler(self.symbol, self.interval, self.mock_callback)

    @patch('websocket.WebSocketApp')
    def test_data_handler_init(self, MockWebSocketApp):
        self.assertEqual(self.data_handler.symbol, self.symbol.lower())
        self.assertEqual(self.data_handler.interval, self.interval)
        self.assertEqual(self.data_handler.callback, self.mock_callback)
        self.assertIn(self.symbol.lower(), self.data_handler.ws_url)
        self.assertIn(self.interval, self.data_handler.ws_url)
        self.assertIsNone(self.data_handler.ws)
        self.assertEqual(self.data_handler.reconnect_interval, 5)
        self.assertFalse(self.data_handler.is_running)
        self.assertIsNone(self.data_handler.thread)

    def test_on_message_closed_kline(self):
        mock_ws = MagicMock()
        # Example Binance kline message for a closed kline
        message = {
            "e": "kline",
            "E": 1678886400000,
            "s": "BTCUSDT",
            "k": {
                "t": 1678886400000,
                "o": "20000.00",
                "h": "20100.00",
                "l": "19900.00",
                "c": "20050.00",
                "v": "10.00",
                "x": True # Closed kline
            }
        }
        self.data_handler._on_message(mock_ws, json.dumps(message))
        self.mock_callback.assert_called_once()
        called_data = self.mock_callback.call_args[0][0]
        self.assertIsInstance(called_data, OCHLVData)
        self.assertEqual(called_data.timestamp, 1678886400000)
        self.assertEqual(called_data.close, Decimal("20050.00"))

    def test_on_message_open_kline(self):
        mock_ws = MagicMock()
        # Example Binance kline message for an open kline
        message = {
            "e": "kline",
            "E": 1678886400000,
            "s": "BTCUSDT",
            "k": {
                "t": 1678886400000,
                "o": "20000.00",
                "h": "20100.00",
                "l": "19900.00",
                "c": "20050.00",
                "v": "10.00",
                "x": False # Open kline
            }
        }
        self.data_handler._on_message(mock_ws, json.dumps(message))
        self.mock_callback.assert_not_called() # Should not call callback for open kline

    @patch('time.sleep', return_value=None) # Mock sleep to speed up test
    @patch('websocket.WebSocketApp')
    def test_on_close_reconnect(self, MockWebSocketApp, mock_sleep):
        self.data_handler.is_running = True
        self.data_handler._connect_websocket = MagicMock() # Mock this to prevent actual connection
        self.data_handler._on_close(MagicMock(), 1000, "Normal Closure")
        mock_sleep.assert_called_once_with(self.data_handler.reconnect_interval)
        self.data_handler._connect_websocket.assert_called_once()

    @patch('websocket.WebSocketApp')
    def test_on_close_no_reconnect_if_not_running(self, MockWebSocketApp):
        self.data_handler.is_running = False
        self.data_handler._connect_websocket = MagicMock()
        self.data_handler._on_close(MagicMock(), 1000, "Normal Closure")
        self.data_handler._connect_websocket.assert_not_called()

    @patch('websocket.WebSocketApp')
    @patch('threading.Thread')
    def test_start_stops_and_joins_thread(self, MockThread, MockWebSocketApp):
        mock_ws_instance = MockWebSocketApp.return_value
        mock_thread_instance = MockThread.return_value

        self.data_handler.ws = mock_ws_instance
        self.data_handler.thread = mock_thread_instance
        self.data_handler.is_running = True

        self.data_handler.stop()

        self.assertFalse(self.data_handler.is_running)
        mock_ws_instance.close.assert_called_once()
        mock_thread_instance.join.assert_called_once()

    @patch('websocket.WebSocketApp')
    @patch('threading.Thread')
    def test_start_starts_thread(self, MockThread, MockWebSocketApp):
        mock_thread_instance = MockThread.return_value
        self.data_handler.start()
        self.assertTrue(self.data_handler.is_running)
        MockThread.assert_called_once_with(target=self.data_handler._connect_websocket)
        mock_thread_instance.start.assert_called_once()

if __name__ == '__main__':
    unittest.main()
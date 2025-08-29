import websocket # type: ignore
import json
import threading
import time
from decimal import Decimal
from models import OCHLVData # Import from models.py

class DataHandler:
    def __init__(self, symbol: str, interval: str, callback):
        self.symbol = symbol.lower()
        self.interval = interval
        self.callback = callback
        self.ws_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@kline_{self.interval}"
        self.ws = None
        self.reconnect_interval = 5  # seconds
        self.is_running = False
        self.thread = None

    def _on_message(self, ws, message):
        json_message = json.loads(message)
        kline = json_message['k']
        if kline['x']:  # 'x' indicates if the kline is closed
            ochlv_data = OCHLVData(
                timestamp=kline['t'],
                open=Decimal(kline['o']),
                close=Decimal(kline['c']),
                high=Decimal(kline['h']),
                low=Decimal(kline['l']),
                volume=Decimal(kline['v'])
            )
            self.callback(ochlv_data)

    def _on_error(self, ws, error):
        print(f"WebSocket error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        print(f"WebSocket closed: {close_status_code} - {close_msg}")
        if self.is_running:
            print(f"Attempting to reconnect in {self.reconnect_interval} seconds...")
            time.sleep(self.reconnect_interval)
            self._connect_websocket()

    def _on_open(self, ws):
        print(f"WebSocket opened for {self.symbol}@{self.interval}")

    def _connect_websocket(self):
        self.ws = websocket.WebSocketApp(
            self.ws_url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open
        )
        self.ws.run_forever()

    def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self._connect_websocket)
        self.thread.start()

    def stop(self):
        self.is_running = False
        if self.ws:
            self.ws.close()
        if self.thread:
            self.thread.join()
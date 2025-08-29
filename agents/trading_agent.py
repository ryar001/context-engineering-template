from data.data_handler import DataHandler
from analysis.technical_analyzer import TechnicalAnalyzer
from analysis.strategy import TradingStrategy
from trading.risk_manager import RiskManager
from trading.trader import Trader
from models import OCHLVData
from decimal import Decimal
import time
import logging

logger = logging.getLogger(__name__)

class TradingAgent:
    def __init__(self, symbol: str, interval: str, initial_balance: Decimal):
        self.symbol = symbol
        self.interval = interval
        self.technical_analyzer = TechnicalAnalyzer()
        self.strategy = TradingStrategy(self.technical_analyzer)
        self.risk_manager = RiskManager(account_balance=initial_balance)
        self.trader = Trader()
        self.data_handler = DataHandler(symbol, interval, self._process_ochlv_data)
        self.in_position = False # To track if the bot is currently in a trade

    def _process_ochlv_data(self, ochlv_data: OCHLVData):
        logger.info(f"Received OCHLV data for {self.symbol}: {ochlv_data.close}")
        signal = self.strategy.generate_signal(ochlv_data)

        if signal:
            logger.info(f"Generated signal: {signal.action}")
            if signal.action == 'enter' and not self.in_position:
                # Assuming we are buying the base asset (e.g., BTC in BTCUSDT)
                # Need to get current balance of quote asset (e.g., USDT)
                usdt_balance = self.trader.get_account_balance('USDT').free
                logger.info(f"Current USDT balance: {usdt_balance}")

                # Calculate position size
                try:
                    if signal.stop_loss is None: # Add this check
                        raise ValueError("Stop loss price is required for position size calculation.")

                    position_size = self.risk_manager.calculate_position_size(
                        entry_price=ochlv_data.close,
                        stop_loss_price=signal.stop_loss # Now guaranteed not to be None
                    )
                    # Ensure position size is not greater than available balance
                    # This is a simplification, real calculation needs to consider min notional, step size etc.
                    if position_size * ochlv_data.close > usdt_balance:
                        position_size = usdt_balance / ochlv_data.close
                    
                    logger.info(f"Calculated position size: {position_size}")

                    if position_size > 0:
                        # Place a market buy order
                        order = self.trader.place_market_order(
                            symbol=self.symbol,
                            side='BUY',
                            quantity=position_size
                        )
                        logger.info(f"Placed BUY order: {order}")
                        self.in_position = True
                        # In a real system, you would also place stop-loss and take-profit orders here
                        # For simplicity, we'll assume these are handled by the exchange or a more advanced order management system
                        # self.trader.place_stop_loss_limit_order(...)
                        # self.trader.place_limit_order(...)
                except ValueError as e:
                    logger.error(f"Error calculating position size: {e}")

            elif signal.action == 'exit' and self.in_position:
                # Assuming we are selling the base asset (e.g., BTC in BTCUSDT)
                # Need to get current balance of base asset
                base_asset = self.symbol.replace('USDT', '') # e.g., BTC from BTCUSDT
                base_balance = self.trader.get_account_balance(base_asset).free
                logger.info(f"Current {base_asset} balance: {base_balance}")

                if base_balance > 0:
                    # Place a market sell order
                    order = self.trader.place_market_order(
                        symbol=self.symbol,
                        side='SELL',
                        quantity=base_balance
                    )
                    logger.info(f"Placed SELL order: {order}")
                    self.in_position = False

    def start(self):
        logger.info(f"Starting Trading Agent for {self.symbol}@{self.interval}")
        self.data_handler.start()
        try:
            while True:
                time.sleep(1) # Keep the main thread alive
        except KeyboardInterrupt:
            logger.info("Stopping Trading Agent...")
            self.data_handler.stop()
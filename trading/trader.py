from binance.client import Client # type: ignore
from config.settings import settings
from models import AccountBalance, OrderInfo
from decimal import Decimal

class Trader:
    def __init__(self):
        self.client = Client(settings.BINANCE_API_KEY, settings.BINANCE_API_SECRET, testnet=True)

    def get_account_balance(self, asset: str) -> AccountBalance:
        account_info = self.client.get_asset_balance(asset=asset) # type: ignore
        return AccountBalance(
            asset=asset,
            free=Decimal(account_info['free']),
            locked=Decimal(account_info['locked'])
        )

    def get_open_orders(self, symbol: str | None = None) -> list[OrderInfo]:
        open_orders = self.client.get_open_orders(symbol=symbol)
        orders = []
        for order in open_orders:
            orders.append(OrderInfo(
                symbol=order['symbol'],
                orderId=order['orderId'],
                price=Decimal(order['price']),
                origQty=Decimal(order['origQty']),
                executedQty=Decimal(order['executedQty']),
                status=order['status'],
                side=order['side'],
                type=order['type']
            ))
        return orders

    def place_market_order(self, symbol: str, side: str, quantity: Decimal) -> dict:
        """
        Places a market order.
        side: 'BUY' or 'SELL'
        """
        order = self.client.order_market(
            symbol=symbol,
            side=side,
            quantity=float(quantity) # Binance API expects float for quantity
        )
        return order

    def place_limit_order(self, symbol: str, side: str, quantity: Decimal, price: Decimal) -> dict:
        """
        Places a limit order.
        side: 'BUY' or 'SELL'
        """
        order = self.client.order_limit(
            symbol=symbol,
            side=side,
            quantity=float(quantity),
            price=f"{price:.8f}" # Ensure proper precision for price
        )
        return order

    def place_stop_loss_limit_order(self, symbol: str, side: str, quantity: Decimal, price: Decimal, stop_price: Decimal) -> dict:
        """
        Places a stop loss limit order.
        side: 'BUY' or 'SELL'
        """
        order = self.client.order_stop_loss_limit(
            symbol=symbol,
            side=side,
            quantity=float(quantity),
            price=f"{price:.8f}",
            stopPrice=f"{stop_price:.8f}"
        )
        return order

    def cancel_order(self, symbol: str, order_id: int) -> dict:
        """
        Cancels an open order.
        """
        result = self.client.cancel_order(
            symbol=symbol,
            orderId=order_id
        )
        return result
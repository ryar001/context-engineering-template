from decimal import Decimal

class RiskManager:
    def __init__(self, account_balance: Decimal, risk_per_trade_percentage: Decimal = Decimal('0.10')):
        self.account_balance = account_balance
        self.risk_per_trade_percentage = risk_per_trade_percentage

    def calculate_position_size(self, entry_price: Decimal, stop_loss_price: Decimal) -> Decimal:
        if stop_loss_price >= entry_price:
            raise ValueError("Stop loss price must be less than entry price for a long position.")

        # Calculate the maximum amount of capital to risk on this trade
        max_risk_amount = self.account_balance * self.risk_per_trade_percentage

        # Calculate the risk per unit (e.g., per share or per coin)
        risk_per_unit = entry_price - stop_loss_price

        if risk_per_unit <= 0:
            raise ValueError("Risk per unit must be positive.")

        # Calculate the position size
        position_size = max_risk_amount / risk_per_unit

        return position_size

    def update_account_balance(self, new_balance: Decimal):
        self.account_balance = new_balance
import unittest
from decimal import Decimal
from trading.risk_manager import RiskManager

class TestRiskManager(unittest.TestCase):

    def test_calculate_position_size_valid(self):
        risk_manager = RiskManager(account_balance=Decimal('10000'))
        entry_price = Decimal('100')
        stop_loss_price = Decimal('99') # 1% risk per unit
        expected_position_size = Decimal('10000') * Decimal('0.10') / (Decimal('100') - Decimal('99'))
        self.assertEqual(risk_manager.calculate_position_size(entry_price, stop_loss_price), expected_position_size)

    def test_calculate_position_size_zero_risk_per_unit(self):
        risk_manager = RiskManager(account_balance=Decimal('10000'))
        entry_price = Decimal('100')
        stop_loss_price = Decimal('100')
        with self.assertRaises(ValueError) as cm:
            risk_manager.calculate_position_size(entry_price, stop_loss_price)
        self.assertEqual(str(cm.exception), "Stop loss price must be less than entry price for a long position.")

    def test_calculate_position_size_stop_loss_above_entry(self):
        risk_manager = RiskManager(account_balance=Decimal('10000'))
        entry_price = Decimal('100')
        stop_loss_price = Decimal('101')
        with self.assertRaises(ValueError) as cm:
            risk_manager.calculate_position_size(entry_price, stop_loss_price)
        self.assertEqual(str(cm.exception), "Stop loss price must be less than entry price for a long position.")

    def test_update_account_balance(self):
        risk_manager = RiskManager(account_balance=Decimal('10000'))
        new_balance = Decimal('12000')
        risk_manager.update_account_balance(new_balance)
        self.assertEqual(risk_manager.account_balance, new_balance)

if __name__ == '__main__':
    unittest.main()
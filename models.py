from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class OCHLVData(BaseModel):
    timestamp: int
    open: Decimal
    close: Decimal
    high: Decimal
    low: Decimal
    volume: Decimal

class TradeSignal(BaseModel):
    action: str  # 'enter' or 'exit'
    stop_loss: Optional[Decimal] = None
    take_profit: Optional[Decimal] = None

class AccountBalance(BaseModel):
    asset: str
    free: Decimal
    locked: Decimal

class OrderInfo(BaseModel):
    symbol: str
    orderId: int
    price: Decimal
    origQty: Decimal
    executedQty: Decimal
    status: str
    side: str
    type: str

class SymbolInfo(BaseModel):
    exchange: str
    global_symbol: str
    price_ccy: str
    price_quote_ccy: str
    exchange_symbol: str
    size_ccy: str
    size_multiplier: Decimal
    market_type: str
    is_live: bool
    order_size_incremental: Decimal
    min_order_size: Decimal
    min_order_size_in_value: Decimal
    tick_size: Decimal
    expiry_datetime: Optional[str] = None
    update_datetime: Optional[str] = None
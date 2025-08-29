import requests
from typing import List, Dict, Optional
from decimal import Decimal
from models import SymbolInfo

class SymbolInfoManager:
    def __init__(self, base_url: str = "https://testnet.binance.vision"):
        self.base_url = base_url
        self.exchange_info_endpoint = "/api/v3/exchangeInfo"
        self.symbols_info: Dict[str, SymbolInfo] = {} # Cache for symbol info

    def fetch_exchange_info(self) -> List[SymbolInfo]:
        url = f"{self.base_url}{self.exchange_info_endpoint}"
        try:
            response = requests.get(url)
            response.raise_for_status() # Raise an exception for HTTP errors
            data = response.json()
            
            parsed_symbols = []
            for symbol_data in data.get("symbols", []):
                # Extract filters for min_qty, step_size, min_notional, tick_size
                min_order_size = Decimal('0')
                order_size_incremental = Decimal('0')
                min_order_size_in_value = Decimal('0')
                tick_size = Decimal('0')

                for f in symbol_data.get('filters', []):
                    if f['filterType'] == 'LOT_SIZE':
                        min_order_size = Decimal(f.get('minQty', '0'))
                        order_size_incremental = Decimal(f.get('stepSize', '0'))
                    elif f['filterType'] == 'MIN_NOTIONAL':
                        min_order_size_in_value = Decimal(f.get('minNotional', '0'))
                    elif f['filterType'] == 'PRICE_FILTER':
                        tick_size = Decimal(f.get('tickSize', '0'))

                # Determine market_type
                market_type = "SPOT" # Default for spot API

                # Determine is_live
                is_live = symbol_data.get('status') == 'TRADING'

                # Construct global_symbol (example: FX-ETH/USDT for ETHUSDT)
                # This is a simplification and might need more complex logic for other exchanges/types
                global_symbol = f"FX-{symbol_data['baseAsset']}/{symbol_data['quoteAsset']}"

                parsed_symbols.append(SymbolInfo(
                    exchange="BINANCE_SPOT", # Assuming Binance Spot for this project
                    global_symbol=global_symbol,
                    price_ccy=symbol_data['baseAsset'],
                    price_quote_ccy=symbol_data['quoteAsset'],
                    exchange_symbol=symbol_data['symbol'],
                    size_ccy=symbol_data['baseAsset'], # For spot, size_ccy is typically baseAsset
                    size_multiplier=Decimal('1'), # For spot, 1 contract value is 1
                    market_type=market_type,
                    is_live=is_live,
                    order_size_incremental=order_size_incremental,
                    min_order_size=min_order_size,
                    min_order_size_in_value=min_order_size_in_value,
                    tick_size=tick_size,
                    expiry_datetime=None, # Not applicable for spot
                    update_datetime=None # Binance exchangeInfo doesn't provide this per symbol
                ))
            self.symbols_info = {s.exchange_symbol: s for s in parsed_symbols}
            return parsed_symbols
        except requests.exceptions.RequestException as e:
            print(f"Error fetching exchange info: {e}")
            return []

    def get_symbol_info(self, exchange_symbol: str) -> Optional[SymbolInfo]:
        if not self.symbols_info:
            self.fetch_exchange_info() # Fetch if not already cached
        return self.symbols_info.get(exchange_symbol.upper())
# AI Trading Chatbot with Technical Analysis - Planning Document

## Project Overview
This project aims to build an AI-powered trading chatbot that uses technical analysis, price action, and volume analysis to make trading decisions. The bot will execute trades on the Binance Spot Testnet and follow strict risk management rules. It also includes a chat interface for users to query their account information.

## Core Principles
1.  **Data-Driven Decisions**: All trading decisions must be based on OCHLV data analysis.
2.  **Real-time Processing**: Utilize WebSockets for low-latency market data.
3.  **Safety First**: Implement robust risk management and use the testnet for all trading operations.
4.  **Modularity**: Structure the code into logical components (data handling, analysis, trading, etc.).
5.  **Testability**: Write unit and integration tests to validate each part of the system.

## Goal
Create a CLI-based AI trading chatbot that can:
1.  Process real-time OCHLV data via WebSockets for a given trading pair.
2.  Analyze the data using technical indicators, price action, and volume.
3.  Decide on trading actions: `enter` or `exit`.
4.  Calculate and set `stop loss` and `take profit` levels for each entry.
5.  Execute orders on the Binance Spot Testnet.
6.  Adhere to a strict risk management rule: never risk more than 10% of the account value on a single trade.
7.  Provide a chat interface to query account information like balance and orders.

## Desired Codebase Structure
```bash
.
├───data/
│   └───data_handler.py         # Handles fetching and processing OCHLV data from WebSockets
├───analysis/
│   ├───technical_analyzer.py   # Implements technical indicators
│   └───strategy.py             # The core trading strategy logic
├───trading/
│   ├───trader.py               # Executes trades and queries account info on the Binance API
│   └───risk_manager.py         # Manages risk and position sizing
├───agents/
│   ├───trading_agent.py        # The main agent that orchestrates the bot
│   └───query_agent.py          # The agent that handles user queries about their account
├───config/
│   └───settings.py             # For API keys and other configurations
├───tests/
│   ├───test_data_handler.py
│   ├───test_strategy.py
│   └───test_risk_manager.py
├───main.py                     # The entry point for the CLI application
└───.env.example                # Template for environment variables
```

## Data Models
```python
from pydantic import BaseModel
from decimal import Decimal
from typing import List

class OCHLVData(BaseModel):
    timestamp: int
    open: Decimal
    close: Decimal
    high: Decimal
    low: Decimal
    volume: Decimal

class TradeSignal(BaseModel):
    action: str  # 'enter' or 'exit'
    stop_loss: Decimal | None = None
    take_profit: Decimal | None = None

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
```

## Known Gotchas & Library Quirks
-   **CRITICAL**: The Binance Testnet has different API keys from the mainnet.
-   **CRITICAL**: Ensure all order types (e.g., MARKET, LIMIT, STOP_LOSS_LIMIT) are supported by the testnet.
-   **CRITICAL**: API rate limits must be handled to avoid getting IP banned.
-   **CRITICAL**: Floating point precision is important for prices and quantities. Use Python's `decimal` module.
-   **CRITICAL**: Store API keys securely in environment variables, never in the code.
-   **CRITICAL**: WebSocket connections can be unstable. Implement reconnection logic.

## Validation Loop
### Level 1: Syntax & Style
```bash
ruff check . --fix
mypy .
```
### Level 2: Unit Tests
```bash
pytest tests/ -v
```
### Level 3: Integration Test
```bash
# Run the bot on the testnet for a short period
python main.py trade --symbol BTCUSDT --interval 1m

# Test the chat interface
python main.py chat
```
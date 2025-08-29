name: "AI Trading Chatbot with Technical Analysis"
description: |
  Build an AI-powered trading chatbot that uses technical analysis, price action, and volume analysis to make trading decisions. The bot will execute trades on the Binance Spot Testnet and follow strict risk management rules. It also includes a chat interface for users to query their account information.

## Core Principles
1.  **Data-Driven Decisions**: All trading decisions must be based on OCHLV data analysis.
2.  **Real-time Processing**: Utilize WebSockets for low-latency market data.
3.  **Safety First**: Implement robust risk management and use the testnet for all trading operations.
4.  **Modularity**: Structure the code into logical components (data handling, analysis, trading, etc.).
5.  **Testability**: Write unit and integration tests to validate each part of the system.

---

## Goal
Create a CLI-based AI trading chatbot that can:
1.  Process real-time OCHLV data via WebSockets for a given trading pair.
2.  Analyze the data using technical indicators, price action, and volume.
3.  Decide on trading actions: `enter` or `exit`.
4.  Calculate and set `stop loss` and `take profit` levels for each entry.
5.  Execute orders on the Binance Spot Testnet.
6.  Adhere to a strict risk management rule: never risk more than 10% of the account value on a single trade.
7.  Provide a chat interface to query account information like balance and orders.

## Why
-   **Business value**: Automate trading strategies and provide a user-friendly way to monitor account status.
-   **Learning**: Provide a hands-on project for learning about AI in trading and API integration.
-   **Problems solved**: Removes emotional decision-making from trading and enforces disciplined risk management.

## What
A CLI application with two modes:
1.  **Trading Mode**: A user can start the trading bot for a specific symbol and time interval. The bot will then autonomously analyze market data in real-time and execute trades.
2.  **Chat Mode**: A user can start a chat interface to ask questions in natural language about their Binance account (e.g., 'what is my BTC balance?', 'show me my open orders').

### Success Criteria
-   [ ] The bot can successfully connect to the Binance Spot Testnet.
-   [ ] The bot can connect to the Binance WebSocket stream and correctly parse incoming OCHLV data.
-   [ ] The analysis module generates trading signals based on its strategy.
-   [ ] The bot can open and close trades with proper stop loss and take profit levels.
-   [ ] The risk management module correctly calculates position sizes.
-   [ ] The chat interface can successfully query and display account balance and open orders.
-   [ ] All tests pass, and the code is well-documented.

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- url: https://testnet.binance.vision/
  why: Main portal for the Binance Spot Testnet.

- url: https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md
  why: Official documentation for Binance WebSocket streams.

- url: https://github.com/binance/binance-spot-api-docs/tree/master/testnet
  why: Official documentation for the Binance Spot Testnet API, including endpoints and authentication.

- url: https://python-binance.readthedocs.io/en/latest/
  why: A popular Python wrapper for the Binance API. It has support for WebSockets.

- url: https://www.investopedia.com/articles/active-trading/092315/understanding-and-using-volume-trading.asp
  why: For understanding volume analysis.

- url: https://www.babypips.com/learn/forex/price-action
  why: For understanding price action.

- url: https://developers.binance.com/docs/binance-spot-api-docs/rest-api/general-endpoints#exchange-information
  why: Official documentation for Binance exchange information endpoint.
```

### Desired Codebase tree with files to be added
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

### Known Gotchas & Library Quirks
```python
# CRITICAL: The Binance Testnet has different API keys from the mainnet.
# CRITICAL: Ensure all order types (e.g., MARKET, LIMIT, STOP_LOSS_LIMIT) are supported by the testnet.
# CRITICAL: API rate limits must be handled to avoid getting IP banned.
# CRITICAL: Floating point precision is important for prices and quantities. Use Python's `decimal` module.
# CRITICAL: Store API keys securely in environment variables, never in the code.
# CRITICAL: WebSocket connections can be unstable. Implement reconnection logic.
```

## Implementation Blueprint

### Data models and structure
```python
# models.py (can be in a separate file or within relevant modules)
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
```

### List of tasks to be completed
```yaml
Task 1: Setup Configuration
CREATE config/settings.py:
  - Use pydantic-settings to load Binance API key and secret from environment variables.
CREATE .env.example:
  - Add `BINANCE_API_KEY` and `BINANCE_API_SECRET`.

Task 2: Real-time Data Handler
CREATE data/data_handler.py:
  - Implement a WebSocket client to connect to the Binance kline stream (e.g., `btcusdt@kline_1m`).
  - The client should receive WebSocket messages, parse the JSON payload, and convert it into the standardized `OCHLVData` Pydantic model.
  - Implement a callback or a queue to pass the standardized data to the `TradingAgent`.
  - Include reconnection logic in case the WebSocket connection drops.

Task 3: Analysis Module
CREATE analysis/technical_analyzer.py:
  - Implement functions for a few technical indicators (e.g., RSI, MACD, Moving Averages).
CREATE analysis/strategy.py:
  - Develop a simple trading strategy that uses the technical indicators, price action, and volume to generate a `TradeSignal`.

Task 4: Risk Management
CREATE trading/risk_manager.py:
  - Implement a function to calculate the position size for a trade based on the 10% risk rule.

Task 5: Trading Module
CREATE trading/trader.py:
  - Implement functions to place orders on the Binance Testnet.
  - Add functions to query account information: `get_account_balance`, `get_open_orders`.

Task 6: Trading Agent
CREATE agents/trading_agent.py:
  - This will be the main loop of the bot.
  - It will receive standardized data from the `DataHandler` and pass it to the `Analysis` module.
  - If a trade signal is generated, it will use the `RiskManager` and `Trader` to execute the trade.

Task 7: Main CLI
CREATE main.py:
  - Create a simple CLI using `argparse` or `click` to start the bot.
  - It should have two subcommands: `trade` and `chat`.

Task 8: Testing
CREATE tests/:
  - Write unit tests for the strategy, risk manager, and data handler.
  - Mock the Binance API calls and WebSocket messages.

Task 9: Create Query Agent and Chat Interface
CREATE agents/query_agent.py:
  - This agent will be responsible for handling user queries.
  - It will have tools that call the functions in `trading/trader.py` to get account information.
MODIFY main.py:
  - Implement the `chat` subcommand to start a chat loop with the `QueryAgent`.

Task 10: Symbol Information Retrieval
CREATE trading/symbol_info_manager.py:
  - Implement a function to fetch exchange information from GET https://testnet.binance.vision/api/v3/exchangeInfo.
  - Parse the response into a list of `SymbolInfo` Pydantic models.
  - Add a function to retrieve symbol information by `exchange_symbol`.
```

## Future Implementations

### LLM-driven Trade Signals
- **Goal**: Integrate a Large Language Model (LLM) to analyze market data, news, and sentiment to generate more sophisticated trade signals.
- **Approach**:
    1.  Develop a prompt engineering strategy to feed relevant market data (OCHLV, technical indicators, news headlines) to the LLM.
    2.  Define the expected output format for LLM-generated signals (e.g., JSON with `action`, `target_price`, `stop_loss_level`, `reasoning`).
    3.  Implement a new module to interact with the LLM API, handle rate limits, and parse its responses.
    4.  Replace or augment the existing `TradingStrategy` with the LLM's signal generation.
    5.  Add robust error handling and fallback mechanisms in case the LLM provides ambiguous or invalid signals.

### LLM-driven Query Agent
- **Goal**: Enhance the `QueryAgent` to understand and respond to natural language queries using an LLM.
- **Approach**:
    1.  Integrate an LLM into the `QueryAgent` to interpret user questions.
    2.  Enable the LLM to intelligently select and utilize the available tools (e.g., `get_account_balance`, `get_open_orders`) based on the user's query.
    3.  Format the LLM's responses to be user-friendly and informative.
    4.  Implement error handling for cases where the LLM cannot fulfill a request or misinterprets a query.

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

# Expected behavior:
# - The bot starts without errors and connects to the WebSocket.
# - It logs that it's receiving and parsing data.
# - It logs when it generates a signal and places a trade.
# - Check the Binance Testnet UI to confirm that orders are being placed.

# Test the chat interface
python main.py chat

# Expected behavior:
# > You: What is my USDT balance?
# > Bot: Your USDT balance is 1000.00 (free: 950.00, locked: 50.00)
# > You: Show me my open orders
# > Bot: You have 1 open order for BTCUSDT...
```

## Confidence Score: 8/10
High confidence because the requirements are clear and the Binance API is well-documented. The use of a Python wrapper library will simplify the implementation. The main challenge will be in developing a profitable trading strategy, but for the purpose of this PRP, a simple strategy is sufficient.

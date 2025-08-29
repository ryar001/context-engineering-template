## 2025-08-29 - AI Trading Chatbot with Technical Analysis
### Task 1: Setup Configuration - COMPLETED
- CREATE config/settings.py:
  - Use pydantic-settings to load Binance API key and secret from environment variables.
- CREATE .env.example:
  - Add `BINANCE_API_KEY` and `BINANCE_API_SECRET`.

### Task 2: Real-time Data Handler - COMPLETED
- CREATE data/data_handler.py:
  - Implement a WebSocket client to connect to the Binance kline stream (e.g., `btcusdt@kline_1m`).
  - The client should receive WebSocket messages, parse the JSON payload, and convert it into the standardized `OCHLVData` Pydantic model.
  - Implement a callback or a queue to pass the standardized data to the `TradingAgent`.
  - Include reconnection logic in case the WebSocket connection drops.

### Task 3: Analysis Module - COMPLETED
- CREATE analysis/technical_analyzer.py:
  - Implement functions for a few technical indicators (e.g., RSI, MACD, Moving Averages).
- CREATE analysis/strategy.py:
  - Develop a simple trading strategy that uses the technical indicators, price action, and volume to generate a `TradeSignal`.

### Task 4: Risk Management - COMPLETED
- CREATE trading/risk_manager.py:
  - Implement a function to calculate the position size for a trade based on the 10% risk rule.

### Task 5: Trading Module - COMPLETED
- CREATE trading/trader.py:
  - Implement functions to place orders on the Binance Testnet.
  - Add functions to query account information: `get_account_balance`, `get_open_orders`.

### Task 6: Trading Agent - COMPLETED
- CREATE agents/trading_agent.py:
  - This will be the main loop of the bot.
  - It will receive standardized data from the `DataHandler` and pass it to the `Analysis` module.
  - If a trade signal is generated, it will use the `RiskManager` and `Trader` to execute the trade.

### Task 7: Main CLI - COMPLETED
- CREATE main.py:
  - Create a simple CLI using `argparse` or `click` to start the bot.
  - It should have two subcommands: `trade` and `chat`.

### Task 8: Testing - COMPLETED
- CREATE tests/:
  - Write unit tests for the strategy, risk manager, and data handler.
  - Mock the Binance API calls and WebSocket messages.
  - Added `test_query_agent.py` to test the QueryAgent, including LLM integration.

### Task 9: Create Query Agent and Chat Interface - COMPLETED
- CREATE agents/query_agent.py:
  - This agent will be responsible for handling user queries.
  - It will have tools that call the functions in `trading/trader.py` to get account information.
  - **LLM Integration**: Enhanced to use Google Gemini for natural language understanding and response generation for queries not directly handled by specific tools.
- MODIFY main.py:
  - Implement the `chat` subcommand to start a chat loop with the `QueryAgent`.

### Task 10: Symbol Information Retrieval - COMPLETED
- CREATE trading/symbol_info_manager.py:
  - Implement a function to fetch exchange information from GET https://testnet.binance.vision/api/v3/exchangeInfo.
  - Parse the response into a list of `SymbolInfo` Pydantic models.
  - Add a function to retrieve symbol information by `exchange_symbol`.
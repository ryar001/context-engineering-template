# AI Trading Chatbot with Technical Analysis

This project implements an AI-powered trading chatbot designed to operate on the Binance Spot Testnet. It leverages technical analysis, price action, and volume analysis to make informed trading decisions, while adhering to strict risk management protocols. The bot also features a chat interface for users to query their account information.

## Features

*   **Real-time Data Processing**: Fetches and processes OCHLV (Open, Close, High, Low, Volume) data via WebSockets for low-latency market insights.
*   **Technical Analysis**: Integrates various technical indicators (e.g., RSI, MACD, Moving Averages) for in-depth market analysis.
*   **Intelligent Trading Strategy**: Employs a sophisticated trading strategy that combines technical indicators, price action, and volume to generate `enter` or `exit` signals.
*   **Robust Risk Management**: Implements a strict risk management rule, ensuring that no more than 10% of the account value is risked on a single trade. Automatically calculates and sets `stop loss` and `take profit` levels.
*   **Binance Testnet Integration**: Executes trades and queries account information securely on the Binance Spot Testnet.
*   **Interactive Chat Interface**: Features an AI-powered conversational interface, leveraging a Large Language Model (LLM) to understand natural language queries and provide intelligent responses regarding account balance, open orders, and other trading information.
*   **Modular Design**: Organized into logical components for data handling, analysis, trading, and agent orchestration, promoting maintainability and scalability.

## Project Structure

```
.
├───data/
│   └───data_handler.py         # Handles fetching and processing OCHLV data from WebSockets
├───analysis/
│   ├───technical_analyzer.py   # Implements technical indicators
│   └───strategy.py             # The core trading strategy logic
├───trading/
│   ├───trader.py               # Executes trades and queries account info on the Binance API
│   ├───risk_manager.py         # Manages risk and position sizing
│   └───symbol_info_manager.py  # Fetches and manages symbol information from Binance
├───agents/
│   ├───trading_agent.py        # Orchestrates the trading bot's operations
│   └───query_agent.py          # Handles user queries about their account
├───config/
│   └───settings.py             # Manages API keys and other configurations
├───tests/
│   ├───test_data_handler.py
│   ├───test_risk_manager.py
│   ├───test_strategy.py
├───main.py                     # The entry point for the CLI application
├───models.py                   # Pydantic models for data structures
├───requirements.txt            # Project dependencies
└───.env.example                # Template for environment variables
```

## Setup

To set up the project, follow these steps:

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/ai-bot-trader.git
    cd ai-bot-trader
    ```

2.  **Create a virtual environment** (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:

    Create a `.env` file in the root directory of the project based on `.env.example`.
    Obtain your Binance Spot Testnet API Key and Secret from [Binance Testnet](https://testnet.binance.vision/).

    ```dotenv
    BINANCE_API_KEY="your_binance_testnet_api_key"
    BINANCE_API_SECRET="your_binance_testnet_api_secret"
    GEMINI_API_KEY="your_gemini_api_key" # Optional, for LLM-powered chat interface
    ```

## Usage

### Running the Trading Bot

To start the trading bot, use the `trade` command with the desired symbol and interval:

```bash
python main.py trade --symbol BTCUSDT --interval 1m --initial_balance 10000
```

*   `--symbol`: The trading pair (e.g., `BTCUSDT`).
*   `--interval`: The kline interval (e.g., `1m`, `5m`, `1h`).
*   `--initial_balance`: (Optional) Your initial account balance for risk management calculations (default: `10000`).

### Using the Chat Interface

To interact with the chatbot and query your account information, use the `chat` command:

```bash
python main.py chat
```

This will start an interactive chat session where you can ask questions about your balance, open orders, etc.

## Testing

To run the unit tests, ensure you have `pytest` installed (included in `requirements.txt`) and execute:

```bash
pytest tests/ -v
```

## Contributing

Contributions are welcome! Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

import argparse
from agents.trading_agent import TradingAgent
from agents.query_agent import QueryAgent
from decimal import Decimal
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="AI Trading Chatbot")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Trade subcommand
    trade_parser = subparsers.add_parser("trade", help="Start the trading bot")
    trade_parser.add_argument("--symbol", type=str, required=True, help="Trading symbol (e.g., BTCUSDT)")
    trade_parser.add_argument("--interval", type=str, default="1m", help="Kline interval (e.g., 1m, 5m, 1h)")
    trade_parser.add_argument("--initial_balance", type=Decimal, default=Decimal('10000'), help="Initial account balance for risk management")

    # Chat subcommand
    chat_parser = subparsers.add_parser("chat", help="Start the chat interface")

    args = parser.parse_args()

    if args.command == "trade":
        agent = TradingAgent(args.symbol, args.interval, args.initial_balance)
        agent.start()
    elif args.command == "chat":
        query_agent = QueryAgent()
        query_agent.start_chat()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
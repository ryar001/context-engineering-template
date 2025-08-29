from trading.trader import Trader
import re
from config.settings import settings
import google.generativeai as genai # Import Gemini library
import logging

logger = logging.getLogger(__name__)
import logging

logger = logging.getLogger(__name__)

class QueryAgent:
    def __init__(self):
        self.trader = Trader()
        self.llm = None
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.llm = genai.GenerativeModel('gemini-pro')
            logger.info("Gemini LLM initialized for QueryAgent.")
        else:
            logger.warning("GEMINI_API_KEY not found. LLM capabilities will be disabled.")

    def process_query(self, query: str) -> str:
        query_lower = query.lower()

        # Existing regex-based logic
        if "balance" in query_lower:
            asset_match = re.search(r"(\w+) balance", query_lower)
            if asset_match:
                asset = asset_match.group(1).upper()
                try:
                    balance = self.trader.get_account_balance(asset)
                    return f"Your {balance.asset} balance is {balance.free + balance.locked} (free: {balance.free}, locked: {balance.locked})"
                except Exception as e:
                    return f"Could not retrieve balance for {asset}. Error: {e}"
            else:
                return "Please specify an asset for balance query (e.g., 'what is my BTC balance?')."
        elif "open orders" in query_lower or "orders" in query_lower:
            symbol_match = re.search(r"open orders for (\w+)", query_lower)
            symbol = symbol_match.group(1).upper() if symbol_match else None
            try:
                orders = self.trader.get_open_orders(symbol)
                if orders:
                    order_details = []
                    for order in orders:
                        order_details.append(
                            f"Symbol: {order.symbol}, ID: {order.orderId}, Side: {order.side}, Type: {order.type}, "
                            f"Price: {order.price}, Original Qty: {order.origQty}, Executed Qty: {order.executedQty}, "
                            f"Status: {order.status}"
                        )
                    return "Your open orders:\n" + "\n".join(order_details)
                else:
                    return "You have no open orders."
            except Exception as e:
                return f"Could not retrieve open orders. Error: {e}"
        elif "hello" in query_lower or "hi" in query_lower:
            return "Hello! How can I assist you with your Binance account today?"
        elif "exit" in query_lower or "quit" in query_lower:
            return "Goodbye!"
        else:
            # If not handled by regex, pass to LLM
            if self.llm:
                try:
                    prompt = (
                        "You are a helpful assistant for a Binance trading bot. "
                        "Your primary function is to answer questions about account balances and open orders. "
                        "If the user asks about something else, politely state that you can only help with account information. "
                        "Here is the user's query: " + query
                    )
                    response = self.llm.generate_content(prompt)
                    return response.text
                except Exception as e:
                    logger.error(f"Error communicating with LLM: {e}")
                    return "I'm sorry, I'm having trouble processing your request at the moment. Please try again later."
            else:
                return "I'm sorry, I can only answer questions about your account balance and open orders. Please try rephrasing your question."

    def start_chat(self):
        print("Starting chat mode. Type 'exit' or 'quit' to end the chat.")
        while True:
            user_query = input("You: ")
            response = self.process_query(user_query)
            print(f"Bot: {response}")
            if response == "Goodbye!":
                break
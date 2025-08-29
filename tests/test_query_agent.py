import pytest
from unittest.mock import MagicMock, patch
from agents.query_agent import QueryAgent
from models import AccountBalance, OrderInfo
from decimal import Decimal

# Mock the settings to control GEMINI_API_KEY for testing
@pytest.fixture(autouse=True)
def mock_settings():
    with patch('config.settings.settings') as mock_settings_obj:
        mock_settings_obj.GEMINI_API_KEY = "TEST_GEMINI_KEY"
        yield mock_settings_obj

# Fixture for a QueryAgent instance with mocked Trader and LLM
@pytest.fixture
def query_agent_with_llm():
    with patch('agents.query_agent.Trader') as MockTrader,
         patch('agents.query_agent.genai') as MockGenai:
        
        # Configure MockTrader
        mock_trader_instance = MockTrader.return_value
        mock_trader_instance.get_account_balance.return_value = AccountBalance(asset="BTC", free=Decimal("0.5"), locked=Decimal("0.1"))
        mock_trader_instance.get_open_orders.return_value = [
            OrderInfo(symbol="BTCUSDT", orderId=123, price=Decimal("30000"), origQty=Decimal("0.001"), executedQty=Decimal("0"), status="NEW", side="BUY", type="LIMIT")
        ]

        # Configure MockGenai
        mock_genai_model = MockGenai.GenerativeModel.return_value
        mock_genai_model.generate_content.return_value.text = "I can only help with account information."

        agent = QueryAgent()
        agent.trader = mock_trader_instance # Ensure the agent uses our mock trader
        agent.llm = mock_genai_model # Ensure the agent uses our mock LLM
        yield agent

# Fixture for a QueryAgent instance without LLM (e.g., no API key)
@pytest.fixture
def query_agent_no_llm():
    with patch('config.settings.settings') as mock_settings_obj:
        mock_settings_obj.GEMINI_API_KEY = None
        with patch('agents.query_agent.Trader') as MockTrader:
            agent = QueryAgent()
            agent.trader = MockTrader.return_value
            yield agent


def test_query_agent_init_with_llm(mock_settings):
    # Ensure GEMINI_API_KEY is set for this test
    mock_settings.GEMINI_API_KEY = "TEST_KEY"
    with patch('agents.query_agent.genai') as MockGenai:
        agent = QueryAgent()
        MockGenai.configure.assert_called_once_with(api_key="TEST_KEY")
        MockGenai.GenerativeModel.assert_called_once_with('gemini-pro')
        assert agent.llm is not None

def test_query_agent_init_no_llm(query_agent_no_llm):
    assert query_agent_no_llm.llm is None

def test_process_query_balance(query_agent_with_llm):
    response = query_agent_with_llm.process_query("what is my BTC balance?")
    assert "Your BTC balance is 0.6 (free: 0.5, locked: 0.1)" in response
    query_agent_with_llm.trader.get_account_balance.assert_called_once_with("BTC")

def test_process_query_open_orders(query_agent_with_llm):
    response = query_agent_with_llm.process_query("show me open orders for BTCUSDT")
    assert "Your open orders:" in response
    assert "Symbol: BTCUSDT, ID: 123" in response
    query_agent_with_llm.trader.get_open_orders.assert_called_once_with("BTCUSDT")

def test_process_query_hello(query_agent_with_llm):
    response = query_agent_with_llm.process_query("hello bot")
    assert "Hello! How can I assist you with your Binance account today?" in response

def test_process_query_exit(query_agent_with_llm):
    response = query_agent_with_llm.process_query("quit")
    assert "Goodbye!" in response

def test_process_query_llm_fallback(query_agent_with_llm):
    response = query_agent_with_llm.process_query("What is the weather like today?")
    assert "I can only help with account information." in response
    query_agent_with_llm.llm.generate_content.assert_called_once()

def test_process_query_llm_fallback_no_llm(query_agent_no_llm):
    response = query_agent_no_llm.process_query("Tell me a joke.")
    assert "I'm sorry, I can only answer questions about your account balance and open orders. Please try rephrasing your question." in response
    # Ensure LLM was not called if not initialized
    with patch('agents.query_agent.genai') as MockGenai:
        MockGenai.GenerativeModel.assert_not_called()

## 2025-08-29

### What's New

#### `agents/query_agent.py`
- Implemented an LLM-driven `QueryAgent` to understand and respond to natural language queries.
- Integrated Google Gemini for natural language understanding and response generation.

#### `tests/test_query_agent.py`
- Added unit tests for the `QueryAgent`, covering LLM integration, account balance queries, open order queries, and fallback mechanisms.

#### `main.py`
- Implemented a `chat` subcommand for interactive chat with the `QueryAgent`.

### Refactoring/Improvements

#### `GEMINI.md`
- Standardized command prefix from `--` to `:` for commands in the `./commands` directory.

#### `README.md`
- Rewrote the README.md with a new title, features, project structure, setup instructions, and usage examples for the AI Trading Chatbot.

#### `TASK.md`
- Updated to reflect the completion of the Query Agent and LLM integration tasks.

#### `commands/ai-tracker.md`
- Standardized command prefix from `ai-tracker` to `:ai-tracker` in usage examples.
- Updated workflow steps to reflect `git add -A` and `git diff` for summarization.

#### `PRPs/ai_trading_bot.prp.md`
- Removed duplicate "LLM-driven Query Agent" and "LLM-driven Trade Signals" sections.

# Project Updates

## 2025-08-29

### What's New

#### `AGENT_IMPLEMENTATION_GUIDE.md`

- Added a comprehensive guide for Context Engineering, detailing its principles, workflow, template structure, and best practices for AI coding assistants.
- Includes sections on prompt engineering vs. context engineering, step-by-step setup, writing effective `INITIAL.md` files, the PRP workflow, and using examples effectively.
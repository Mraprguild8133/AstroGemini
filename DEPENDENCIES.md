# Project Dependencies

This document lists all the dependencies required for the Multi-AI Telegram Bot.

## Core Dependencies

### Required Packages
```
python-telegram-bot>=20.0
google-genai>=0.7.0
together>=1.0.0
```

### Package Details

**python-telegram-bot (>=20.0)**
- Official Telegram Bot API wrapper
- Handles all Telegram interactions, webhooks, and message processing
- Includes async support for high performance

**google-genai (>=0.7.0)**
- Google's official Python client for Gemini AI
- Provides access to Gemini 2.5 Flash and other models
- Handles multimodal AI capabilities

**together (>=1.0.0)**
- Together AI's Python client
- Access to open-source models (Llama, Mistral, CodeLlama, Qwen)
- Chat completion API support

## Auto-Installed Dependencies

These packages are automatically installed with the core dependencies:

```
aiohttp>=3.8.0          # HTTP client for async operations
httpx>=0.24.0           # Modern HTTP client
certifi>=2023.0.0       # SSL certificate verification
frozenlist>=1.3.0       # Immutable list implementation
multidict>=6.0.0        # Multi-value dictionary
yarl>=1.8.0             # URL parsing and manipulation
attrs>=22.0.0           # Classes without boilerplate
aiosignal>=1.2.0        # Async signal handling
```

## Installation on Replit

Dependencies are managed through Replit's package manager. The following packages have been installed:

```bash
uv add python-telegram-bot  # Telegram bot framework
uv add google-genai         # Gemini AI integration  
uv add together             # Together AI integration
```

## Environment Variables Required

```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here      # Required
GEMINI_API_KEY=your_gemini_key_here         # Required
TOGETHER_API_KEY=your_together_key_here     # Optional
```

## Optional Configuration Variables

```bash
# Rate Limiting
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60

# Conversation Settings
MAX_CONVERSATION_LENGTH=20

# AI Model Settings
GEMINI_MODEL=gemini-2.5-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=1000

TOGETHER_DEFAULT_MODEL=meta-llama/Llama-2-70b-chat-hf
TOGETHER_TEMPERATURE=0.7
TOGETHER_MAX_TOKENS=1000

# Bot Settings
BOT_USERNAME=GeminiAIBot
BOT_DESCRIPTION=AI Assistant powered by Gemini AI

# Admin Settings
ADMIN_USER_IDS=123456789,987654321
```

## Deployment Requirements

For deploying outside of Replit, create a standard `requirements.txt`:

```txt
python-telegram-bot>=20.0
google-genai>=0.7.0
together>=1.0.0
```

Then install with:
```bash
pip install -r requirements.txt
```

## Python Version

- **Minimum:** Python 3.8+
- **Recommended:** Python 3.11+
- **Current Replit Environment:** Python 3.11

## Package Compatibility

All packages are compatible and tested together:
- No version conflicts
- All support async/await patterns
- Production-ready and stable releases
# Overview

This repository contains a Telegram bot powered by Google's Gemini AI and Together AI that provides intelligent conversational responses to users. The bot supports multiple AI services, allowing users to switch between different models and providers. It handles user messages, maintains conversation context, implements rate limiting to prevent abuse, and provides administrative commands for bot management. It's designed as a scalable, modular system that can be easily deployed and configured through environment variables.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Bot Architecture
The system follows a modular design pattern with clear separation of concerns:

- **TelegramGeminiBot** (`bot.py`): Main bot controller that handles Telegram API interactions, command routing, AI service switching, and orchestrates communication between different services
- **GeminiService** (`gemini_service.py`): Dedicated service layer for Google Gemini AI API integration, responsible for generating intelligent responses with conversation context
- **TogetherService** (`together_service.py`): Service layer for Together AI API integration, providing access to multiple open-source AI models including Llama, Mistral, and CodeLlama
- **RateLimiter** (`rate_limiter.py`): Token bucket algorithm implementation to prevent API abuse and manage user request quotas
- **Config** (`config.py`): Centralized configuration management using environment variables for easy deployment across different environments

## Data Management
The bot uses in-memory storage for conversation history, storing user conversations in a simple dictionary structure. This approach prioritizes simplicity and quick response times but conversations are lost on bot restart. The conversation history is maintained per user with configurable message limits to manage memory usage.

## Rate Limiting Strategy
Implements a sliding window rate limiter using collections.deque for efficient timestamp management. Each user gets a separate request bucket, and old requests are automatically cleaned up to maintain performance. This prevents API quota exhaustion and ensures fair usage across all users.

## Error Handling and Logging
The system includes comprehensive logging with both file and console output. All major components have error handling for graceful degradation when external services are unavailable.

# External Dependencies

## APIs and Services
- **Google Gemini AI API**: Primary AI service for generating intelligent responses, requires GEMINI_API_KEY
- **Together AI API**: Secondary AI service providing access to multiple open-source models, requires TOGETHER_API_KEY (optional)
- **Telegram Bot API**: Primary interface for receiving and sending messages, requires TELEGRAM_BOT_TOKEN

## Python Libraries
- **python-telegram-bot**: Official Telegram bot framework for handling webhooks, commands, and message processing
- **google-genai**: Google's official Python client for Gemini AI API integration
- **together**: Together AI's Python client for accessing multiple open-source AI models

## Configuration Requirements
All external service credentials and bot behavior settings are configured through environment variables, making the system deployment-ready for containerized environments. Key variables include API keys, rate limiting parameters, conversation settings, AI service preferences, and optional admin user configurations.

## New Features (August 2025)
- **Multi-AI Support**: Users can switch between Gemini AI and Together AI using `/ai` command
- **Model Selection**: Access to multiple AI models including Llama, Mistral, CodeLlama, and Qwen through Together AI
- **Dynamic AI Switching**: Per-user AI preference storage with seamless switching between services
- **Extended Commands**: New `/ai` and `/models` commands for AI service management
- **Webhook Support**: Added webhook server for deployment on Render.com and other cloud platforms
- **Deployment Ready**: Complete deployment configuration with Flask webhook server and Render.com setup
- **Docker Support**: Complete containerization with Docker and Docker Compose for any cloud platform
- **Production Scaling**: Multi-deployment options (Replit, Render.com, Docker, VPS) with comprehensive guides
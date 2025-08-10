#!/usr/bin/env python3
"""
Main entry point for the Telegram bot powered by Gemini AI.
This script initializes and starts the bot.
"""

import logging
import os
from bot import TelegramGeminiBot

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler('bot.log'),
            logging.StreamHandler()
        ]
    )

def main():
    """Main function to start the Telegram bot."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Check for required environment variables
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not telegram_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is required")
        return
    
    if not gemini_api_key:
        logger.error("GEMINI_API_KEY environment variable is required")
        return
    
    logger.info("Starting Telegram Gemini AI Bot...")
    
    # Initialize and start the bot
    bot = TelegramGeminiBot(telegram_token)
    bot.run()

if __name__ == "__main__":
    main()

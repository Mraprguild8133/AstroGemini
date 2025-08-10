#!/usr/bin/env python3
"""
Main entry point for webhook-based Telegram bot deployment.
Designed for Render.com and other cloud platforms.
"""

import logging
import os
from webhook_server import TelegramWebhookBot

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.StreamHandler()  # Only console logging for cloud deployment
        ]
    )

def main():
    """Main function to start the webhook bot."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Check for required environment variables
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    webhook_url = os.getenv("WEBHOOK_URL")  # Your Render.com app URL
    
    if not telegram_token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is required")
        return
    
    if not gemini_api_key:
        logger.error("GEMINI_API_KEY environment variable is required")
        return
    
    if not webhook_url:
        logger.error("WEBHOOK_URL environment variable is required for webhook mode")
        logger.info("Set WEBHOOK_URL to your Render.com app URL (e.g., https://yourapp.onrender.com)")
        return
    
    # Get port from environment (Render.com provides this)
    port = int(os.getenv("PORT", 5000))
    
    logger.info("Starting Telegram Gemini AI Bot in webhook mode...")
    logger.info(f"Webhook URL: {webhook_url}")
    logger.info(f"Port: {port}")
    
    # Initialize and start the webhook bot
    bot = TelegramWebhookBot(telegram_token, webhook_url)
    bot.run_webhook(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()
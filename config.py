"""
Configuration settings for the Telegram Gemini AI bot.
"""

import os

class Config:
    """Configuration class containing all bot settings."""
    
    # Rate limiting settings
    RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "10"))  # Max requests per window
    RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))      # Time window in seconds
    
    # Conversation settings
    MAX_CONVERSATION_LENGTH = int(os.getenv("MAX_CONVERSATION_LENGTH", "20"))  # Max messages to keep in memory
    
    # Gemini AI settings
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    GEMINI_TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
    GEMINI_MAX_TOKENS = int(os.getenv("GEMINI_MAX_TOKENS", "1000"))
    
    # Together AI settings
    TOGETHER_DEFAULT_MODEL = os.getenv("TOGETHER_DEFAULT_MODEL", "meta-llama/Llama-2-70b-chat-hf")
    TOGETHER_TEMPERATURE = float(os.getenv("TOGETHER_TEMPERATURE", "0.7"))
    TOGETHER_MAX_TOKENS = int(os.getenv("TOGETHER_MAX_TOKENS", "1000"))
    
    # Bot settings
    BOT_USERNAME = os.getenv("BOT_USERNAME", "GeminiAIBot")
    BOT_DESCRIPTION = os.getenv("BOT_DESCRIPTION", "AI Assistant powered by Gemini AI")
    
    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "bot.log")
    
    # Admin settings (optional)
    ADMIN_USER_IDS = [
        int(uid.strip()) for uid in os.getenv("ADMIN_USER_IDS", "").split(",") 
        if uid.strip().isdigit()
    ]
    
    @classmethod
    def is_admin(cls, user_id: int) -> bool:
        """Check if a user is an admin."""
        return user_id in cls.ADMIN_USER_IDS
    
    @classmethod
    def get_bot_info(cls) -> dict:
        """Get bot information for status commands."""
        return {
            "username": cls.BOT_USERNAME,
            "description": cls.BOT_DESCRIPTION,
            "model": cls.GEMINI_MODEL,
            "rate_limit": f"{cls.RATE_LIMIT_REQUESTS} requests per {cls.RATE_LIMIT_WINDOW} seconds",
            "max_conversation_length": cls.MAX_CONVERSATION_LENGTH
        }

"""
Telegram bot implementation with Gemini AI integration.
Handles user messages, commands, and bot lifecycle.
"""

import logging
from typing import Dict, List
from telegram import Update
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes
)

from gemini_service import GeminiService
from together_service import TogetherService
from rate_limiter import RateLimiter
from config import Config

class TelegramGeminiBot:
    """Main bot class handling Telegram interactions and Gemini AI responses."""
    
    def __init__(self, token: str):
        """Initialize the bot with the provided token."""
        self.token = token
        self.logger = logging.getLogger(__name__)
        
        # Initialize AI services
        self.gemini_service = GeminiService()
        try:
            self.together_service = TogetherService()
            self.together_available = True
        except ValueError as e:
            self.logger.warning(f"Together AI not available: {e}")
            self.together_service = None
            self.together_available = False
        
        self.rate_limiter = RateLimiter()
        
        # Simple in-memory conversation storage
        # Format: {user_id: [{"role": "user/assistant", "content": "message"}]}
        self.conversations: Dict[int, List[Dict[str, str]]] = {}
        
        # User AI preferences: {user_id: "gemini" or "together"}
        self.user_ai_preference: Dict[int, str] = {}
        
        # Initialize the application
        self.application = Application.builder().token(token).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up command and message handlers."""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("clear", self.clear_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("ai", self.ai_command))
        self.application.add_handler(CommandHandler("models", self.models_command))
        
        # Message handler for text messages
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command."""
        user = update.effective_user
        ai_services = "Gemini AI"
        if self.together_available:
            ai_services += " and Together AI"
        
        welcome_message = (
            f"👋 Hello {user.first_name}!\n\n"
            f"I'm an AI assistant powered by {ai_services}. I can help you with:\n"
            "• Answering questions\n"
            "• Writing and editing text\n"
            "• Explaining complex topics\n"
            "• Creative tasks\n"
            "• General conversation\n\n"
            "Just send me a message and I'll respond intelligently!\n\n"
            "Use /help to see available commands."
        )
        await update.message.reply_text(welcome_message)
        self.logger.info(f"User {user.id} ({user.username}) started the bot")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command."""
        ai_info = "Gemini AI"
        if self.together_available:
            ai_info = "Gemini AI and Together AI"
        
        help_text = (
            f"🤖 *AI Assistant Commands*\n\n"
            "/start - Start the bot and see welcome message\n"
            "/help - Show this help message\n"
            "/clear - Clear conversation history\n"
            "/status - Check bot status\n"
            "/ai - Switch between AI services (gemini/together)\n"
            "/models - Show available AI models\n\n"
            "*How to use:*\n"
            f"Just send me any text message and I'll respond using {ai_info}!\n\n"
            "*Features:*\n"
            f"• Intelligent responses powered by {ai_info}\n"
            "• Conversation memory within your session\n"
            "• Rate limiting for fair usage\n"
            "• Error handling and reliability\n\n"
            "Need help? Just ask me anything!"
        )
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /clear command to reset conversation history."""
        user_id = update.effective_user.id
        if user_id in self.conversations:
            del self.conversations[user_id]
        
        await update.message.reply_text(
            "🗑️ Conversation history cleared! Starting fresh."
        )
        self.logger.info(f"User {user_id} cleared conversation history")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /status command to show bot status."""
        user_id = update.effective_user.id
        conversation_length = len(self.conversations.get(user_id, []))
        current_ai = self.user_ai_preference.get(user_id, "gemini")
        
        gemini_status = "⚡ Connected" if self.gemini_service else "❌ Not Available"
        together_status = "⚡ Connected" if self.together_available else "❌ Not Available"
        
        status_text = (
            "🟢 *Bot Status: Active*\n\n"
            f"📊 Your conversation messages: {conversation_length}\n"
            f"🔄 Total active conversations: {len(self.conversations)}\n"
            f"🤖 Current AI: {current_ai.title()}\n"
            f"🧠 Gemini AI: {gemini_status}\n"
            f"🚀 Together AI: {together_status}\n"
            f"📡 Telegram API: Connected\n\n"
            "Everything is working perfectly!"
        )
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def ai_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /ai command to switch between AI services."""
        user_id = update.effective_user.id
        args = context.args
        
        if not args:
            current_ai = self.user_ai_preference.get(user_id, "gemini")
            available_ais = ["gemini"]
            if self.together_available:
                available_ais.append("together")
            
            ai_text = (
                f"🤖 *Current AI: {current_ai.title()}*\n\n"
                f"Available AI services: {', '.join(available_ais)}\n\n"
                "To switch AI service, use:\n"
                "/ai gemini - Use Gemini AI\n"
            )
            if self.together_available:
                ai_text += "/ai together - Use Together AI\n"
            
            await update.message.reply_text(ai_text, parse_mode='Markdown')
            return
        
        ai_choice = args[0].lower()
        
        if ai_choice == "gemini":
            self.user_ai_preference[user_id] = "gemini"
            await update.message.reply_text("🧠 Switched to Gemini AI!")
        elif ai_choice == "together" and self.together_available:
            self.user_ai_preference[user_id] = "together"
            await update.message.reply_text("🚀 Switched to Together AI!")
        elif ai_choice == "together" and not self.together_available:
            await update.message.reply_text("❌ Together AI is not available. Please check the TOGETHER_API_KEY.")
        else:
            await update.message.reply_text("❌ Invalid AI service. Use 'gemini' or 'together'.")
    
    async def models_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /models command to show available models."""
        models_text = "🤖 *Available AI Models*\n\n"
        
        models_text += "*Gemini AI:*\n• gemini-2.5-flash (default)\n\n"
        
        if self.together_available:
            models_text += "*Together AI Models:*\n"
            together_models = self.together_service.get_available_models()
            for name, model_id in together_models.items():
                models_text += f"• {name}: {model_id.split('/')[-1]}\n"
            models_text += "\nUse /ai together to switch to Together AI models."
        else:
            models_text += "*Together AI:* Not available (missing API key)"
        
        await update.message.reply_text(models_text, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages from users."""
        user = update.effective_user
        user_id = user.id
        message_text = update.message.text
        
        self.logger.info(f"Received message from {user.username} ({user_id}): {message_text[:50]}...")
        
        # Check rate limiting
        if not self.rate_limiter.is_allowed(user_id):
            await update.message.reply_text(
                "⚠️ You're sending messages too quickly. Please wait a moment before trying again."
            )
            return
        
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        try:
            # Get conversation history
            conversation_history = self.conversations.get(user_id, [])
            
            # Add user message to conversation history
            conversation_history.append({"role": "user", "content": message_text})
            
            # Determine which AI service to use
            user_ai = self.user_ai_preference.get(user_id, "gemini")
            
            # Generate response using selected AI service
            if user_ai == "together" and self.together_available:
                response = await self.together_service.generate_response(
                    message_text, 
                    conversation_history
                )
            else:
                # Default to Gemini AI
                response = await self.gemini_service.generate_response(
                    message_text, 
                    conversation_history
                )
            
            # Add assistant response to conversation history
            conversation_history.append({"role": "assistant", "content": response})
            
            # Update conversation history (keep last 10 messages to manage memory)
            self.conversations[user_id] = conversation_history[-Config.MAX_CONVERSATION_LENGTH:]
            
            # Send response to user
            await update.message.reply_text(response)
            
            self.logger.info(f"Sent response to {user.username} ({user_id})")
            
        except Exception as e:
            self.logger.error(f"Error processing message from {user_id}: {str(e)}")
            await update.message.reply_text(
                "❌ I'm having trouble processing your message right now. "
                "Please try again in a moment. If the problem persists, "
                "contact the administrator."
            )
    
    def run(self):
        """Start the bot with polling."""
        self.logger.info("Bot is starting...")
        try:
            self.application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )
        except Exception as e:
            self.logger.error(f"Critical error running bot: {str(e)}")
            raise

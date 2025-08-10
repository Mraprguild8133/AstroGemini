"""
Together AI service for generating intelligent responses using various AI models.
Handles communication with Together AI API.
"""

import logging
import os
from typing import List, Dict, Optional
from together import Together

class TogetherService:
    """Service class for interacting with Together AI API."""
    
    def __init__(self):
        """Initialize the Together AI service with API client."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize Together client
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            raise ValueError("TOGETHER_API_KEY environment variable is required")
        
        self.client = Together(api_key=api_key)
        
        # Available models - you can change these based on your needs
        self.available_models = {
            "llama": "meta-llama/Llama-2-70b-chat-hf",
            "mistral": "mistralai/Mixtral-8x7B-Instruct-v0.1", 
            "codellama": "codellama/CodeLlama-34b-Instruct-hf",
            "qwen": "Qwen/Qwen1.5-72B-Chat"
        }
        
        # Default model
        self.default_model = self.available_models["llama"]
        
        # System instruction for the bot
        self.system_instruction = (
            "You are a helpful, intelligent AI assistant in a Telegram bot. "
            "Provide clear, accurate, and helpful responses to user questions. "
            "Be conversational but professional. Keep responses concise but informative. "
            "If you're unsure about something, acknowledge it honestly. "
            "Avoid generating harmful, inappropriate, or misleading content."
        )
    
    def _format_conversation_for_together(self, conversation_history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Format conversation history for Together AI API.
        
        Args:
            conversation_history: List of messages in format [{"role": "user/assistant", "content": "text"}]
        
        Returns:
            Formatted messages for Together AI
        """
        messages = [{"role": "system", "content": self.system_instruction}]
        
        if conversation_history:
            for msg in conversation_history:
                role = "user" if msg["role"] == "user" else "assistant"
                messages.append({"role": role, "content": msg["content"]})
        
        return messages
    
    async def generate_response(self, message: str, conversation_history: List[Dict[str, str]] = None, model_name: str = None) -> str:
        """
        Generate a response using Together AI.
        
        Args:
            message: The user's message
            conversation_history: List of previous messages
            model_name: Specific model to use (llama, mistral, codellama, qwen)
        
        Returns:
            Generated response text
        """
        try:
            # Select model
            if model_name and model_name in self.available_models:
                model = self.available_models[model_name]
            else:
                model = self.default_model
            
            # Prepare conversation history
            messages = self._format_conversation_for_together(conversation_history or [])
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            self.logger.info(f"Generating response with {model} for message: {message[:50]}...")
            
            # Generate response using Together AI
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
                top_p=0.8,
            )
            
            if response and response.choices and len(response.choices) > 0:
                response_text = response.choices[0].message.content.strip()
                self.logger.info("Successfully generated response with Together AI")
                return response_text
            else:
                self.logger.warning("Empty response from Together AI")
                return "I'm sorry, I couldn't generate a response right now. Please try again."
                
        except Exception as e:
            self.logger.error(f"Error generating response with Together AI: {str(e)}")
            
            # Provide specific error messages based on the type of error
            error_message = "I'm experiencing technical difficulties with Together AI. Please try again in a moment."
            
            if "quota" in str(e).lower() or "limit" in str(e).lower():
                error_message = "I've reached my Together AI quota limit. Please try again later."
            elif "authentication" in str(e).lower() or "api key" in str(e).lower():
                error_message = "There's an authentication issue with Together AI service. Please contact the administrator."
            elif "network" in str(e).lower() or "connection" in str(e).lower():
                error_message = "I'm having network connectivity issues with Together AI. Please try again in a moment."
            
            return f"❌ {error_message}"
    
    def get_available_models(self) -> Dict[str, str]:
        """Get list of available models."""
        return self.available_models.copy()
    
    def is_healthy(self) -> bool:
        """
        Check if the Together AI service is healthy by making a simple test request.
        
        Returns:
            True if service is healthy, False otherwise
        """
        try:
            messages = [
                {"role": "system", "content": self.system_instruction},
                {"role": "user", "content": "Hello"}
            ]
            
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=messages,
                max_tokens=50
            )
            
            return bool(response and response.choices)
        except Exception as e:
            self.logger.error(f"Together AI health check failed: {str(e)}")
            return False
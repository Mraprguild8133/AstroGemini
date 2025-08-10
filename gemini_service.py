"""
Gemini AI service for generating intelligent responses.
Handles communication with Google's Gemini API.
"""

import logging
import os
from typing import List, Dict
from google import genai
from google.genai import types

class GeminiService:
    """Service class for interacting with Gemini AI API."""
    
    def __init__(self):
        """Initialize the Gemini service with API client."""
        self.logger = logging.getLogger(__name__)
        
        # Initialize Gemini client
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"
        
        # System instruction for the bot
        self.system_instruction = (
            "You are a helpful, intelligent AI assistant in a Telegram bot. "
            "Provide clear, accurate, and helpful responses to user questions. "
            "Be conversational but professional. Keep responses concise but informative. "
            "If you're unsure about something, acknowledge it honestly. "
            "Avoid generating harmful, inappropriate, or misleading content."
        )
    
    async def generate_response(self, message: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Generate a response using Gemini AI.
        
        Args:
            message: The user's message
            conversation_history: List of previous messages in format [{"role": "user/assistant", "content": "text"}]
        
        Returns:
            Generated response text
        """
        try:
            # Prepare the conversation context
            contents = []
            
            # Add conversation history if available
            if conversation_history:
                for msg in conversation_history[:-1]:  # Exclude the current message as it's already included
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))
            
            # Add the current message
            contents.append(types.Content(role="user", parts=[types.Part(text=message)]))
            
            self.logger.info(f"Generating response for message: {message[:50]}...")
            
            # Generate response
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=0.7,
                    max_output_tokens=1000,
                    top_p=0.8,
                    top_k=40
                )
            )
            
            if response.text:
                self.logger.info("Successfully generated response")
                return response.text.strip()
            else:
                self.logger.warning("Empty response from Gemini API")
                return "I'm sorry, I couldn't generate a response right now. Please try again."
                
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            
            # Provide specific error messages based on the type of error
            error_message = "I'm experiencing technical difficulties. Please try again in a moment."
            
            if "quota" in str(e).lower() or "limit" in str(e).lower():
                error_message = "I've reached my API quota limit. Please try again later."
            elif "authentication" in str(e).lower() or "api key" in str(e).lower():
                error_message = "There's an authentication issue with my AI service. Please contact the administrator."
            elif "network" in str(e).lower() or "connection" in str(e).lower():
                error_message = "I'm having network connectivity issues. Please try again in a moment."
            
            return f"❌ {error_message}"
    
    def is_healthy(self) -> bool:
        """
        Check if the Gemini service is healthy by making a simple test request.
        
        Returns:
            True if service is healthy, False otherwise
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents="Hello",
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    max_output_tokens=50
                )
            )
            return bool(response.text)
        except Exception as e:
            self.logger.error(f"Health check failed: {str(e)}")
            return False

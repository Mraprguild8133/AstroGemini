"""
Rate limiter implementation to prevent API abuse and manage usage.
"""

import time
from typing import Dict
from collections import defaultdict, deque
from config import Config

class RateLimiter:
    """Simple rate limiter using token bucket algorithm."""
    
    def __init__(self):
        """Initialize the rate limiter."""
        # Store request timestamps for each user
        self.user_requests: Dict[int, deque] = defaultdict(lambda: deque())
        
        # Configuration
        self.max_requests = Config.RATE_LIMIT_REQUESTS
        self.time_window = Config.RATE_LIMIT_WINDOW
    
    def is_allowed(self, user_id: int) -> bool:
        """
        Check if a user is allowed to make a request based on rate limits.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            True if request is allowed, False if rate limited
        """
        current_time = time.time()
        user_requests = self.user_requests[user_id]
        
        # Remove old requests outside the time window
        while user_requests and user_requests[0] <= current_time - self.time_window:
            user_requests.popleft()
        
        # Check if user has exceeded rate limit
        if len(user_requests) >= self.max_requests:
            return False
        
        # Add current request timestamp
        user_requests.append(current_time)
        return True
    
    def get_remaining_requests(self, user_id: int) -> int:
        """
        Get the number of remaining requests for a user.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Number of remaining requests in current window
        """
        current_time = time.time()
        user_requests = self.user_requests[user_id]
        
        # Remove old requests outside the time window
        while user_requests and user_requests[0] <= current_time - self.time_window:
            user_requests.popleft()
        
        return max(0, self.max_requests - len(user_requests))
    
    def get_reset_time(self, user_id: int) -> float:
        """
        Get the time when rate limit will reset for a user.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Unix timestamp when rate limit resets
        """
        user_requests = self.user_requests[user_id]
        
        if not user_requests:
            return time.time()
        
        # Rate limit resets when the oldest request falls out of the window
        return user_requests[0] + self.time_window
    
    def cleanup_old_data(self):
        """Clean up old request data to prevent memory leaks."""
        current_time = time.time()
        users_to_remove = []
        
        for user_id, requests in self.user_requests.items():
            # Remove old requests
            while requests and requests[0] <= current_time - self.time_window:
                requests.popleft()
            
            # If no recent requests, mark user for removal
            if not requests:
                users_to_remove.append(user_id)
        
        # Remove users with no recent activity
        for user_id in users_to_remove:
            del self.user_requests[user_id]

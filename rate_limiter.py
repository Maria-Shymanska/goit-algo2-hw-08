import random
from typing import Dict
import time
from collections import deque

class SlidingWindowRateLimiter:
    def __init__(self, window_size: int = 10, max_requests: int = 1):
        # Initialize the rate limiter with a time window and max requests allowed in that window
        self.window_size = window_size
        self.max_requests = max_requests
        # Dictionary to store user_id -> deque of timestamps of their messages
        self.users_requests: Dict[str, deque] = {}

    def _cleanup_window(self, user_id: str, current_time: float) -> None:
        """
        Remove timestamps of messages that are outside the current sliding window.
        If no timestamps remain, remove the user from tracking.
        """
        if user_id not in self.users_requests:
            return
        
        window = self.users_requests[user_id]
        # Remove all timestamps older than the start of the sliding window
        while window and window[0] <= current_time - self.window_size:
            window.popleft()
        
        # Remove user from dictionary if no recent messages remain
        if not window:
            del self.users_requests[user_id]

    def can_send_message(self, user_id: str) -> bool:
        """
        Check if the user can send a message at the current time.
        Returns True if message can be sent, False otherwise.
        """
        current_time = time.time()
        self._cleanup_window(user_id, current_time)
        
        if user_id not in self.users_requests:
            # User has no previous messages in window, so allowed to send
            return True
        
        # Check if the count of messages in the window is less than max allowed
        return len(self.users_requests[user_id]) < self.max_requests

    def record_message(self, user_id: str) -> bool:
        """
        Record a new message from the user if allowed.
        Returns True if message recorded (allowed), False if rate limited.
        """
        current_time = time.time()
        self._cleanup_window(user_id, current_time)
        
        if self.can_send_message(user_id):
            if user_id not in self.users_requests:
                self.users_requests[user_id] = deque()
            self.users_requests[user_id].append(current_time)
            return True
        else:
            return False

    def time_until_next_allowed(self, user_id: str) -> float:
        """
        Returns the time in seconds the user must wait until next message is allowed.
        Returns 0 if a message can be sent immediately.
        """
        current_time = time.time()
        if user_id not in self.users_requests:
            return 0.0
        
        self._cleanup_window(user_id, current_time)
        if user_id not in self.users_requests:
            return 0.0
        
        window = self.users_requests[user_id]
        if len(window) < self.max_requests:
            return 0.0
        
        earliest = window[0]
        wait_time = self.window_size - (current_time - earliest)
        return max(wait_time, 0.0)


# Demonstration function
def test_rate_limiter():
    # Create a rate limiter with 10 second window and max 1 message allowed
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)

    print("\n=== Message stream simulation ===")
    for message_id in range(1, 11):
        user_id = message_id % 5 + 1

        allowed = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(f"Message {message_id:2d} | User {user_id} | "
              f"{'✓' if allowed else f'× (wait {wait_time:.1f}s)'}")

        time.sleep(random.uniform(0.1, 1.0))

    print("\nWaiting 4 seconds...")
    time.sleep(4)

    print("\n=== New message batch after waiting ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        allowed = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(f"Message {message_id:2d} | User {user_id} | "
              f"{'✓' if allowed else f'× (wait {wait_time:.1f}s)'}")
        time.sleep(random.uniform(0.1, 1.0))


if __name__ == "__main__":
    test_rate_limiter()

import time
from typing import Dict
import random

class ThrottlingRateLimiter:
    def __init__(self, min_interval: float = 10.0):
        # Dictionary to store the timestamp of the last message per user
        self.min_interval = min_interval
        self.user_last_message_time: Dict[str, float] = {}

    def can_send_message(self, user_id: str) -> bool:
        """
        Check if the user can send a message based on the throttling interval.
        """
        current_time = time.time()

        # First message is always allowed
        if user_id not in self.user_last_message_time:
            return True

        last_time = self.user_last_message_time[user_id]
        return (current_time - last_time) >= self.min_interval

    def record_message(self, user_id: str) -> bool:
        """
        Record a message if allowed. Returns True if the message is recorded,
        otherwise False (message throttled).
        """
        if self.can_send_message(user_id):
            self.user_last_message_time[user_id] = time.time()
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        """
        Return the time remaining until the user is allowed to send the next message.
        Returns 0.0 if a message can be sent immediately.
        """
        if user_id not in self.user_last_message_time:
            return 0.0

        current_time = time.time()
        last_time = self.user_last_message_time[user_id]
        remaining_time = self.min_interval - (current_time - last_time)
        return max(0.0, remaining_time)


def test_throttling_limiter():
    limiter = ThrottlingRateLimiter(min_interval=10.0)

    print("\n=== Message stream simulation (Throttling) ===")
    for message_id in range(1, 11):
        user_id = message_id % 5 + 1

        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(f"Message {message_id:2d} | User {user_id} | "
              f"{'✓' if result else f'× (wait {wait_time:.1f}s)'}")

        # Random delay between messages
        time.sleep(random.uniform(0.1, 1.0))

    print("\nWaiting 10 seconds...")
    time.sleep(10)

    print("\n=== New message batch after waiting ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(f"Message {message_id:2d} | User {user_id} | "
              f"{'✓' if result else f'× (wait {wait_time:.1f}s)'}")
        time.sleep(random.uniform(0.1, 1.0))


if __name__ == "__main__":
    test_throttling_limiter()

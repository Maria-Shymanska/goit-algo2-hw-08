# Rate Limiter Implementations in Python

This project contains two different rate limiter implementations in Python, simulating common techniques used in backend systems to manage traffic and prevent abuse:

1. **Token Bucket Rate Limiter** — controls the number of requests over time using tokens.
2. **Throttling Rate Limiter** — enforces a fixed interval between messages to prevent chat spam.

---

## Task 1: Token Bucket Rate Limiter

### Description

Implements a **Token Bucket** algorithm that limits the number of requests a user can make over time. Each user has their own token bucket that refills at a specified rate. A request is allowed only if a token is available.

### Features

- Each user has an independent token bucket.
- Bucket has a maximum capacity (`max_tokens`) and refill rate (`refill_rate`).
- Tokens are added based on elapsed time since the last request.
- Requests without available tokens are denied.

### Usage

- Class: `TokenBucketRateLimiter`
- Key Methods:
  - `can_proceed(user_id: str) -> bool`: Returns `True` if the request is allowed.
  - `add_tokens(user_id: str)`: Refills the token bucket based on time.
- Includes a `test_token_bucket()` function that simulates 30 user requests with random delays.

---

## Task 2: Throttling Rate Limiter for Chat

### Description

Implements a **Throttling** mechanism to limit how frequently users can send chat messages. This ensures users must wait a fixed minimum interval between messages.

### Features

- Fixed waiting time (`min_interval`) between messages for each user.
- First message from any user is always allowed.
- Message is denied if sent before the interval has passed.
- Provides exact remaining wait time until the next allowed message.

### Usage

- Class: `ThrottlingRateLimiter`
- Key Methods:
  - `can_send_message(user_id: str) -> bool`: Checks if the user can send a message.
  - `record_message(user_id: str) -> bool`: Records the message time if allowed.
  - `time_until_next_allowed(user_id: str) -> float`: Returns seconds until the user can send the next message.
- Includes a `test_throttling_limiter()` function that simulates message bursts from multiple users and validates behavior.

---

## Requirements

- Python 3.7+
- Standard libraries only (no external dependencies)

---

## How to Run

```bash
python rate_limiter.py
```

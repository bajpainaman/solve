# Webhook retries

Webhook delivery retries a failed request up to 5 times. The retries use exponential backoff from 2 seconds to 32 seconds, so they do not overwhelm the receiver. An event that fails all 5 retries moves to a dead-letter queue, where you can inspect it later. You should monitor the depth of that queue.

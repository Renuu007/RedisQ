#!/usr/bin/env python3
"""
Simple example showing how to use RedisQ
"""

import time
import requests
from redisq import threaded_worker, RedisQueueBackend, fifo

# 1. Define your tasks with the @fifo decorator
@fifo(queue="email-queue")
def send_email(recipient, subject, body):
    print(f"📧 Sending email to {recipient}: {subject}")
    time.sleep(0.5)  # Simulate email sending delay
    print(f"✅ Email sent to {recipient}")
    return f"Email sent to {recipient}"

@fifo(queue="webhook-queue")
def send_webhook(url, data):
    print(f"🌐 Sending webhook to {url}")
    try:
        response = requests.post(url, json=data, timeout=10)  # Send HTTP POST with timeout
        print(f"✅ Webhook sent to {url}: {response.status_code}")
        return f"Webhook sent: {response.status_code}"
    except Exception as e:
        print(f"❌ Webhook failed: {e}")
        return f"Webhook failed: {e}"

# 2. Initialize the worker (after decorating functions)
print("🚀 Starting RedisQ...")
backend = RedisQueueBackend("redis://localhost:6379")  # Connect to Redis server
worker = threaded_worker(backend=backend)  # Start worker threads

# 3. Queue some tasks
print("\n📝 Queueing tasks...")

# These will execute in order within each queue
send_email("user1@example.com", "Welcome!", "Welcome to our service")
send_email("user2@example.com", "Newsletter", "Monthly newsletter")
send_email("user3@example.com", "Reminder", "Don't forget to check in")

# These will execute in parallel to emails (different queue)
send_webhook("https://httpbin.org/post", {"event": "user_signup", "user_id": 123})
send_webhook("https://httpbin.org/post", {"event": "order_placed", "order_id": 456})

print("⏳ Processing tasks...")
time.sleep(8)  # Wait for tasks to complete

print("\n🎉 All tasks completed!")

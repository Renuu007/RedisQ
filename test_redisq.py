#!/usr/bin/env python3
"""
Test script for RedisQ - Simple Redis-backed FIFO task queue
"""

import time
import logging
import requests
import redis
import os
from redisq import threaded_worker, RedisQueueBackend, fifo

# Enable debug logging to see what's happening
logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

# Global list to track execution order
execution_order = []

print("🚀 Starting RedisQ Test...")

def wait_for_redis(redis_url, max_retries=5, delay=1):
    """Wait for Redis to be available"""
    print("⏳ Waiting for Redis to be ready...")
    for attempt in range(max_retries):
        try:
            r = redis.from_url(redis_url)
            r.ping()
            print("✅ Redis is ready!")
            return True
        except (redis.ConnectionError, redis.TimeoutError) as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Redis not ready yet... ({e})")
            time.sleep(delay)
    print("❌ Redis failed to start after maximum retries")
    return False

# Get Redis URL from environment or use default
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")  # Use environment variable

# Wait for Redis to be ready before proceeding
if not wait_for_redis(redis_url):
    exit(1)

# 1. Define test functions FIRST (so they get registered)
@fifo(queue="test-queue")
def test_task_1():
    print("✅ Executing Task 1")
    execution_order.append("Task 1")  # Track execution order
    time.sleep(0.1)  # Simulate some work
    return "Task 1 completed"

@fifo(queue="test-queue")
def test_task_2():
    print("✅ Executing Task 2")
    execution_order.append("Task 2")  # Track execution order
    time.sleep(0.1)  # Simulate some work
    return "Task 2 completed"

@fifo(queue="test-queue")
def test_task_3():
    print("✅ Executing Task 3")
    execution_order.append("Task 3")  # Track execution order
    time.sleep(0.1)  # Simulate some work
    return "Task 3 completed"

@fifo(queue="http-queue")
def make_http_request(url):
    print(f"🌐 Making HTTP request to {url}")
    try:
        response = requests.get(url, timeout=5)  # HTTP GET with timeout
        print(f"📄 Response from {url}: {response.status_code}")
        execution_order.append(f"HTTP {url}")  # Track execution order
        return f"HTTP request to {url} completed with status {response.status_code}"
    except Exception as e:
        print(f"❌ HTTP request to {url} failed: {e}")
        execution_order.append(f"HTTP {url} (failed)")  # Track failed requests
        return f"HTTP request to {url} failed: {e}"

# 2. NOW initialize the worker (after functions are decorated)
print("📡 Initializing Redis backend...")
backend = RedisQueueBackend(redis_url)  # Connect to Redis

print("🔧 Starting threaded worker...")
worker = threaded_worker(backend=backend)  # Start worker threads

# Give threads a moment to start
time.sleep(1)

# 3. Queue some tasks
print("\n📝 Queueing tasks...")
test_task_1()  # Add to queue
test_task_2()  # Add to queue
test_task_3()  # Add to queue

# Queue some HTTP requests
make_http_request("https://httpbin.org/get")  # Add HTTP task
make_http_request("https://jsonplaceholder.typicode.com/posts/1")  # Add HTTP task

print("⏳ Waiting for tasks to complete...")
time.sleep(5)  # Wait longer for tasks to execute

# 4. Check results
print("\n📊 Test Results:")
print(f"Tasks executed in order: {execution_order}")

# Verify FIFO order
if len(execution_order) >= 3 and execution_order[:3] == ["Task 1", "Task 2", "Task 3"]:
    print("✅ FIFO order preserved for test-queue!")
else:
    print("❌ FIFO order NOT preserved for test-queue!")

if len(execution_order) >= 5:
    print("✅ HTTP requests executed!")
else:
    print("⚠️  Some HTTP requests may not have completed yet")

print("\n🎉 RedisQ test completed!")
print(f"📈 Total tasks executed: {len(execution_order)}")

# Let's also test Redis connectivity directly
print("\n🔍 Testing Redis connectivity...")
try:
    redis_client = backend.redis  # Get Redis client
    redis_client.ping()  # Test connection
    print("✅ Redis connection successful!")
    
    # Check if there are any items in our queues
    test_queue_length = redis_client.llen("test-queue")  # Get queue length
    http_queue_length = redis_client.llen("http-queue")  # Get queue length
    print(f"📊 test-queue length: {test_queue_length}")
    print(f"📊 http-queue length: {http_queue_length}")
    
except Exception as e:
    print(f"❌ Redis connection failed: {e}")

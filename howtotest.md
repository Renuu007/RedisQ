# How to Test RedisQ

This guide explains how to test RedisQ to ensure it's working correctly in your environment.

## Prerequisites

Before testing, make sure you have:

1. **Redis server running** (either locally or via Docker)
2. **Python 3.9+** installed
3. **RedisQ installed** (see installation section below)

## Quick Redis Setup

### Option 1: Docker (Recommended)
```bash
# Start Redis in Docker
docker run -d --name redis-test -p 6379:6379 redis:7-alpine

# Verify Redis is running
docker ps | grep redis
```

### Option 2: Local Redis Installation
```bash
# On Windows (using Chocolatey)
choco install redis-64

# On macOS (using Homebrew)
brew install redis
redis-server

# On Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis
```

## Installing RedisQ

Since RedisQ isn't on PyPI yet, install it in development mode:

```bash
# Clone the repository
git clone https://github.com/Renuu007/RedisQ.git
cd RedisQ

# Install in development mode
pip install -e .

# Or install dependencies manually
pip install redis>=4.0.0
```

## Running the Tests

### 1. Basic Functionality Test

Create a simple test file (`test_basic.py`):

```python
import time
from redisq import threaded_worker, RedisQueueBackend, fifo

# Define test functions FIRST
@fifo(queue="test-queue")
def hello_world():
    print("Hello from RedisQ!")
    return "success"

# Initialize worker
backend = RedisQueueBackend("redis://localhost:6379")
worker = threaded_worker(backend=backend)

# Queue and execute
hello_world()
time.sleep(2)  # Wait for execution
print("Test completed!")
```

Run it:
```bash
python test_basic.py
```

Expected output:
```
Hello from RedisQ!
Test completed!
```

### 2. FIFO Order Test

Create `test_fifo.py`:

```python
import time
from redisq import threaded_worker, RedisQueueBackend, fifo

execution_order = []

@fifo(queue="order-test")
def task_1():
    execution_order.append("Task 1")
    print("✅ Task 1 executed")

@fifo(queue="order-test")
def task_2():
    execution_order.append("Task 2")
    print("✅ Task 2 executed")

@fifo(queue="order-test")
def task_3():
    execution_order.append("Task 3")
    print("✅ Task 3 executed")

# Initialize worker
backend = RedisQueueBackend("redis://localhost:6379")
worker = threaded_worker(backend=backend)

# Queue tasks in order
task_1()
task_2()
task_3()

# Wait and verify
time.sleep(3)
print(f"Execution order: {execution_order}")

# Verify FIFO
if execution_order == ["Task 1", "Task 2", "Task 3"]:
    print("✅ FIFO order preserved!")
else:
    print("❌ FIFO order NOT preserved!")
```

### 3. Multiple Queues Test

Create `test_multiple_queues.py`:

```python
import time
from redisq import threaded_worker, RedisQueueBackend, fifo

results = {"email": [], "webhook": []}

@fifo(queue="email-queue")
def send_email(recipient):
    results["email"].append(recipient)
    print(f"📧 Email sent to {recipient}")

@fifo(queue="webhook-queue")
def send_webhook(url):
    results["webhook"].append(url)
    print(f"🌐 Webhook sent to {url}")

# Initialize worker
backend = RedisQueueBackend("redis://localhost:6379")
worker = threaded_worker(backend=backend)

# Queue tasks to different queues
send_email("user1@example.com")
send_webhook("https://api1.example.com")
send_email("user2@example.com")
send_webhook("https://api2.example.com")

# Wait and verify
time.sleep(3)
print(f"Email results: {results['email']}")
print(f"Webhook results: {results['webhook']}")

if len(results["email"]) == 2 and len(results["webhook"]) == 2:
    print("✅ Multiple queues working correctly!")
else:
    print("❌ Multiple queues test failed!")
```

### 4. Error Handling Test

Create `test_errors.py`:

```python
import time
from redisq import threaded_worker, RedisQueueBackend, fifo

@fifo(queue="error-test")
def failing_task():
    print("⚠️ This task will fail")
    raise Exception("Intentional error for testing")

@fifo(queue="error-test")
def working_task():
    print("✅ This task works fine")
    return "success"

# Initialize worker
backend = RedisQueueBackend("redis://localhost:6379")
worker = threaded_worker(backend=backend)

# Queue tasks
failing_task()
working_task()

# Wait and observe
time.sleep(3)
print("Error handling test completed")
```

## Troubleshooting

### Common Issues

1. **Redis Connection Error**
   ```
   redis.exceptions.ConnectionError: Error 10061 connecting to localhost:6379
   ```
   **Solution**: Make sure Redis is running on port 6379

2. **Tasks Not Executing**
   - Ensure you define `@fifo` functions BEFORE calling `threaded_worker()`
   - Wait sufficient time for tasks to complete (use `time.sleep()`)

3. **Import Errors**
   ```
   ModuleNotFoundError: No module named 'redisq'
   ```
   **Solution**: Install RedisQ in development mode with `pip install -e .`

### Debug Mode

Enable debug logging to see what's happening:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your RedisQ code here
```

### Redis Inspection

Check Redis directly:

```bash
# Connect to Redis CLI
redis-cli

# Check queue contents
LLEN your-queue-name
LRANGE your-queue-name 0 -1
```

## Performance Testing

For performance testing, create `test_performance.py`:

```python
import time
from redisq import threaded_worker, RedisQueueBackend, fifo

start_time = time.time()
completed_tasks = 0

@fifo(queue="perf-test")
def fast_task(task_id):
    global completed_tasks
    completed_tasks += 1
    return f"Task {task_id} completed"

# Initialize worker
backend = RedisQueueBackend("redis://localhost:6379")
worker = threaded_worker(backend=backend)

# Queue 100 tasks
print("Queueing 100 tasks...")
for i in range(100):
    fast_task(i)

# Wait and measure
time.sleep(5)
end_time = time.time()

print(f"Completed {completed_tasks} tasks in {end_time - start_time:.2f} seconds")
print(f"Rate: {completed_tasks / (end_time - start_time):.2f} tasks/second")
```

## Cleanup

After testing, clean up Docker containers:

```bash
# Stop and remove Redis container
docker stop redis-test
docker rm redis-test
```

## Next Steps

Once your tests pass:
1. Check out `use.md` for real-world usage examples
2. Review the main `README.md` for comprehensive documentation
3. Look at `example_usage.py` for practical examples

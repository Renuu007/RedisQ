# RedisQ Usage Guide

This guide shows you how to use RedisQ in real-world scenarios with practical examples.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Common Patterns](#common-patterns)
3. [Real-World Examples](#real-world-examples)
4. [Best Practices](#best-practices)
5. [Configuration](#configuration)
6. [Error Handling](#error-handling)

## Basic Usage

### 1. Setup & Initialization

```python
from redisq import threaded_worker, RedisQueueBackend, fifo

# Define your tasks FIRST
@fifo(queue="my-queue")
def my_task():
    print("Hello from RedisQ!")

# Then initialize the worker
backend = RedisQueueBackend("redis://localhost:6379")
worker = threaded_worker(backend=backend)

# Now you can queue tasks
my_task()
```

### 2. Basic Task Definition

```python
@fifo(queue="email-queue")
def send_email(recipient, subject, body):
    """Send an email - this will be queued for execution"""
    # Your email sending logic here
    print(f"Sending email to {recipient}: {subject}")
    return f"Email sent to {recipient}"

# Queue the task
send_email("user@example.com", "Welcome!", "Welcome to our service")
```

## Common Patterns

### 1. Web Application Integration

```python
from flask import Flask, request, jsonify
from redisq import threaded_worker, RedisQueueBackend, fifo

app = Flask(__name__)

# Define background tasks
@fifo(queue="user-actions")
def process_user_signup(user_id, email):
    # Send welcome email
    send_welcome_email(email)
    # Update analytics
    track_user_signup(user_id)
    # Sync with CRM
    sync_user_to_crm(user_id)

@fifo(queue="notifications")
def send_notification(user_id, message):
    # Send push notification
    push_service.send(user_id, message)

# Initialize worker on app startup
backend = RedisQueueBackend("redis://localhost:6379")
worker = threaded_worker(backend=backend)

@app.route('/signup', methods=['POST'])
def signup():
    user_data = request.json
    # Create user in database (fast operation)
    user_id = create_user(user_data)
    
    # Queue background tasks (non-blocking)
    process_user_signup(user_id, user_data['email'])
    send_notification(user_id, "Welcome to our platform!")
    
    return jsonify({"user_id": user_id, "status": "created"})
```

### 2. Data Processing Pipeline

```python
@fifo(queue="data-processing")
def process_csv_file(file_path):
    """Process a CSV file row by row"""
    import pandas as pd
    
    df = pd.read_csv(file_path)
    for index, row in df.iterrows():
        # Process each row
        process_data_row(row.to_dict())
    
    return f"Processed {len(df)} rows from {file_path}"

@fifo(queue="data-processing")
def process_data_row(row_data):
    """Process individual row - maintains order"""
    # Transform data
    transformed = transform_data(row_data)
    # Save to database
    save_to_database(transformed)
    # Update search index
    update_search_index(transformed)
```

### 3. API Rate Limiting

```python
@fifo(queue="api-calls")
def make_api_call(endpoint, data):
    """Make API calls in order to respect rate limits"""
    import requests
    import time
    
    # Rate limiting: 1 request per second
    time.sleep(1)
    
    response = requests.post(endpoint, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API call failed: {response.status_code}")

# Queue multiple API calls - they'll execute in order
for record in database_records:
    make_api_call("https://api.example.com/sync", record)
```

## Real-World Examples

### 1. E-commerce Order Processing

```python
from redisq import threaded_worker, RedisQueueBackend, fifo

@fifo(queue="order-processing")
def process_order(order_id):
    """Process an order through multiple steps"""
    order = get_order(order_id)
    
    # Step 1: Validate inventory
    if not validate_inventory(order):
        raise Exception("Insufficient inventory")
    
    # Step 2: Process payment
    payment_result = process_payment(order)
    if not payment_result.success:
        raise Exception("Payment failed")
    
    # Step 3: Generate shipping label
    shipping_label = generate_shipping_label(order)
    
    # Step 4: Send confirmation email
    send_order_confirmation(order.customer_email, order)
    
    return f"Order {order_id} processed successfully"

@fifo(queue="inventory-updates")
def update_inventory(product_id, quantity_change):
    """Update inventory levels in order"""
    current_stock = get_current_stock(product_id)
    new_stock = current_stock + quantity_change
    update_stock_level(product_id, new_stock)
    
    # Notify if low stock
    if new_stock < 10:
        send_low_stock_alert(product_id)
```

### 2. Social Media Content Processing

```python
@fifo(queue="content-moderation")
def moderate_content(post_id):
    """Moderate user-generated content"""
    post = get_post(post_id)
    
    # Check for inappropriate content
    moderation_result = check_content_safety(post.content)
    
    if moderation_result.safe:
        approve_post(post_id)
        notify_user(post.user_id, "Your post has been approved")
    else:
        reject_post(post_id)
        notify_user(post.user_id, "Your post requires review")

@fifo(queue="social-notifications")
def send_social_notification(user_id, notification_type, data):
    """Send notifications in order to maintain chronology"""
    notification = create_notification(user_id, notification_type, data)
    
    # Send push notification
    send_push_notification(user_id, notification)
    
    # Send email if user prefers
    if user_prefers_email(user_id):
        send_email_notification(user_id, notification)
```

### 3. File Processing System

```python
@fifo(queue="file-processing")
def process_uploaded_file(file_path, user_id):
    """Process uploaded files in order"""
    import os
    
    # Determine file type
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.pdf':
        return process_pdf(file_path, user_id)
    elif file_ext == '.csv':
        return process_csv(file_path, user_id)
    elif file_ext in ['.jpg', '.png', '.gif']:
        return process_image(file_path, user_id)
    else:
        raise Exception(f"Unsupported file type: {file_ext}")

def process_pdf(file_path, user_id):
    # Extract text from PDF
    text = extract_pdf_text(file_path)
    # Run OCR if needed
    if not text:
        text = run_ocr(file_path)
    # Save extracted content
    save_extracted_content(user_id, text)
    return "PDF processed successfully"
```

## Best Practices

### 1. Queue Organization

```python
# ✅ Good: Separate queues by function
@fifo(queue="email-queue")
def send_email(): pass

@fifo(queue="webhook-queue")
def send_webhook(): pass

@fifo(queue="data-processing")
def process_data(): pass

# ❌ Bad: Everything in one queue
@fifo(queue="general-queue")
def send_email(): pass

@fifo(queue="general-queue")
def send_webhook(): pass
```

### 2. Task Sizing

```python
# ✅ Good: Small, focused tasks
@fifo(queue="user-processing")
def send_welcome_email(user_id):
    # Single responsibility
    user = get_user(user_id)
    send_email(user.email, "Welcome!", get_welcome_template())

@fifo(queue="user-processing")
def setup_user_profile(user_id):
    # Another single responsibility
    create_default_profile(user_id)
    assign_default_settings(user_id)

# ❌ Bad: Large, complex tasks
@fifo(queue="user-processing")
def handle_new_user(user_id):
    # Too many responsibilities
    send_welcome_email(user_id)
    setup_user_profile(user_id)
    sync_to_crm(user_id)
    update_analytics(user_id)
    # ... many more operations
```

### 3. Error Handling

```python
@fifo(queue="api-calls")
def make_api_request(url, data):
    import requests
    from requests.exceptions import RequestException
    
    try:
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        # Log the error
        logger.error(f"API request failed: {e}")
        # Could implement retry logic here
        raise
```

## Configuration

### Environment-Based Configuration

```python
import os
from redisq import threaded_worker, RedisQueueBackend

# Configuration
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
REDIS_DB = int(os.getenv('REDIS_DB', 0))

# Initialize with custom configuration
backend = RedisQueueBackend(f"{REDIS_URL}/{REDIS_DB}")
worker = threaded_worker(backend=backend)
```

### Production Configuration

```python
# production_config.py
import os
import logging
from redisq import threaded_worker, RedisQueueBackend

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Production Redis configuration
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
backend = RedisQueueBackend(REDIS_URL)

# Initialize worker
worker = threaded_worker(backend=backend)
```

## Error Handling

### Graceful Degradation

```python
@fifo(queue="notifications")
def send_notification(user_id, message):
    try:
        # Try primary notification service
        primary_service.send(user_id, message)
    except Exception as e:
        logger.warning(f"Primary notification failed: {e}")
        try:
            # Fallback to secondary service
            secondary_service.send(user_id, message)
        except Exception as e2:
            logger.error(f"All notification services failed: {e2}")
            # Store for later retry
            store_failed_notification(user_id, message)
```

### Monitoring & Alerting

```python
@fifo(queue="monitoring")
def check_system_health():
    """Regular health check task"""
    try:
        # Check database
        db_status = check_database_health()
        # Check external APIs
        api_status = check_api_health()
        # Check disk space
        disk_status = check_disk_space()
        
        if not all([db_status, api_status, disk_status]):
            send_alert("System health check failed")
    except Exception as e:
        send_alert(f"Health check error: {e}")
```

## Integration Examples

### Django Integration

```python
# tasks.py
from redisq import threaded_worker, RedisQueueBackend, fifo

@fifo(queue="django-tasks")
def process_user_action(user_id, action):
    from django.contrib.auth.models import User
    user = User.objects.get(id=user_id)
    # Process action
    
# settings.py
REDIS_URL = 'redis://localhost:6379'

# apps.py
from django.apps import AppConfig

class MyAppConfig(AppConfig):
    def ready(self):
        from redisq import threaded_worker, RedisQueueBackend
        backend = RedisQueueBackend(settings.REDIS_URL)
        worker = threaded_worker(backend=backend)
```

### FastAPI Integration

```python
from fastapi import FastAPI
from redisq import threaded_worker, RedisQueueBackend, fifo

app = FastAPI()

@fifo(queue="api-tasks")
def background_task(data):
    # Process data
    return "processed"

# Initialize on startup
@app.on_event("startup")
async def startup_event():
    backend = RedisQueueBackend("redis://localhost:6379")
    worker = threaded_worker(backend=backend)

@app.post("/process")
async def process_data(data: dict):
    background_task(data)
    return {"status": "queued"}
```

Remember: RedisQ is designed for I/O-bound tasks. For CPU-intensive work, consider using a proper task queue like Celery or RQ.

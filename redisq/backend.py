# Redis backend implementation for task queue storage
import logging
import os
import redis
from .task import Task

log = logging.getLogger("redisq.producer")


class RedisQueueBackend:  # @TODO: Subclass Redis instead of from_url
    def __init__(self, redis_url=None):
        # Use environment variable if no URL provided (Docker compatibility)
        if redis_url is None:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        
        self.redis_url = redis_url
        self.redis = redis.Redis.from_url(redis_url)  # Connect to Redis server

    def push(self, queue_name, task):
        log.debug(f"Enqueue {task}")
        self.redis.rpush(queue_name, task.json)  # Add task to end of queue (FIFO)

    def pop(self, queue_name, timeout=1):
        if message := self.redis.blpop(queue_name, timeout=timeout):  # Pop from start of queue
            task = Task.load(*message)  # Deserialize task
            log.debug(f"Dequeue {task}")
            return task

        return None

    def __repr__(self):
        return f"RedisQueueBackend({self.redis_url})"

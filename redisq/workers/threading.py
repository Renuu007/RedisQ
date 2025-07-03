# Threading-based worker implementation for queue processing
import threading
import logging

from redisq.manager import mgr
from redisq.backend import RedisQueueBackend
from redisq.consumer import consume_queue

log = logging.getLogger("redisq.worker")


def threaded_worker(backend: RedisQueueBackend = RedisQueueBackend()):
    log.debug("Starting threaded worker")
    mgr.backend = backend  # Set backend for manager

    for queue in mgr.registry.queues:  # Start thread for each queue
        log.debug(f"Initializing worker thread for queue: {queue}")
        thread = threading.Thread(target=consume_queue, args=(queue,), daemon=True)  # Create daemon thread
        thread.start()  # Start thread

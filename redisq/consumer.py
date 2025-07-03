# Consumer implementation for processing tasks from Redis queues
import logging
import time
from .manager import mgr

log = logging.getLogger("redisq.consumer")


def consume_queue(queue_name):
    log.debug(f"Starting consumer for queue: {queue_name}")

    while True:
        task = mgr.backend.pop(queue_name)  # Get next task from queue
        if task:
            log.debug(f"Dequeue {task}")
            qri = mgr.registry.get_func(task.path)  # Get function from registry

            if qri:
                retval = qri.func(*task.args, **task.kwargs)  # Execute the function
                log.debug(f"Execute {qri.path} (result={retval})")
        else:
            time.sleep(0.1)  # Wait if no tasks available

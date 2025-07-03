# Producer decorator for creating FIFO queued functions
import functools
from .manager import mgr
from .task import Task


def fifo(queue):
    def decorator(func):
        qri = mgr.registry.add_func(func, queue)  # Register function with queue

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            task = Task(queue, {  # Create task object
                "path": qri.path,
                "args": args,
                "kwargs": kwargs,
            })
            mgr.backend.push(task.queue, task)  # Push task to queue

        return wrapper

    return decorator

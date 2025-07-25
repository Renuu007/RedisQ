# Central manager for coordinating queue operations
import logging
from .backend import RedisQueueBackend
from .registry import QueueRegistry

log = logging.getLogger("redisq.manager")


class QueueManager:
    _backend: RedisQueueBackend = None

    def __init__(self):
        self.registry = QueueRegistry()  # Initialize function registry

    @property
    def backend(self):
        return self._backend

    @backend.setter
    def backend(self, backend: RedisQueueBackend):
        self._backend = backend
        log.debug(f"Backend configured: {self._backend}")  # Log backend setup


mgr = QueueManager()  # Global manager instance

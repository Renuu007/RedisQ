# Registry for managing function-to-queue mappings
_qri_registry = {}  # Global registry storage


class QRIMeta(type):
    def __call__(cls, func, queue):
        func_id = f"{func.__module__}.{func.__qualname__}"  # Create unique function ID
        if func in _qri_registry:
            return _qri_registry[func_id]  # Return existing instance

        instance = super().__call__(func, queue)
        instance.path = func_id  # Set function path
        _qri_registry[func_id] = instance  # Store in registry
        return instance


class QueueRegistry:
    class QueueRegistryItem(metaclass=QRIMeta):
        id = None

        def __init__(self, func, queue):
            self.func = func  # Store function reference
            self.queue = queue  # Store queue name

    @property
    def funcs(self):
        for fn, qri in _qri_registry.items():
            yield {qri.path: (qri.func, qri.queue)}  # Yield function mappings

    @property
    def queues(self):
        for qri in _qri_registry.values():
            yield qri.queue  # Yield unique queue names

    def add_func(self, func, queue):
        return self.QueueRegistryItem(func, queue)  # Create registry item

    @classmethod
    def get_func(cls, func_id):
        return _qri_registry[func_id]  # Get function by ID

    def __setitem__(self, func, queue):
        self.add_func(func, queue)  # Dictionary-style assignment

    def __getitem__(self, func):
        return self.get_func(func)  # Dictionary-style access

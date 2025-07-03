# Task data structure for queue operations
import json

class Task:
    def __init__(self, queue, message):
        self.queue = queue
        self.path = message["path"]  # Function path identifier
        self.args = message["args"]  # Function arguments
        self.kwargs = message["kwargs"]  # Function keyword arguments

    @classmethod
    def load(cls, queue, json_str):
        message = json.loads(json_str)  # Parse JSON string
        message["args"] = tuple(message["args"])  # Convert to tuple
        return cls(queue, message)

    @property
    def json(self):
        return json.dumps({  # Serialize task to JSON
            "path": self.path,
            "args": self.args,
            "kwargs": self.kwargs,
        })

    def __repr__(self):
        return f"<Task path={self.path} args={self.args} kwargs={self.kwargs}>"

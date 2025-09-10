from abc import ABC, abstractmethod
from datetime import datetime
import uuid
from loguru import logger

class BaseAgent(ABC):
    def __init__(self, name: str, description: str):
        self.agent_id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.performance_metrics = {}
        self.is_busy = False
        self.created_at = datetime.now()
        logger.info(f"Agent {self.name} ({self.agent_id[:8]}) initialized.")

    @abstractmethod
    async def process(self, task: dict) -> dict:
        pass

    def log_performance(self, metric: str, value: float):
        timestamp = datetime.now()
        if metric not in self.performance_metrics:
            self.performance_metrics[metric] = []
        self.performance_metrics[metric].append({"value": value, "timestamp": timestamp})

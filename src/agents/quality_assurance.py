from typing import Dict, Any
from .base_agent import BaseAgent
from loguru import logger

class QualityAssuranceAgent(BaseAgent):
    """Agent to validate answer quality (mocked)"""

    def __init__(self):
        super().__init__(
            name="QualityAssurance",
            description="Validates response quality"
        )
        logger.info("Quality Assurance Agent initialized (mock)")

    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        response = task.get("response", "")
        original_query = task.get("original_query", "")

        logger.info("Mock quality assessment performed")
        # Always approve in mock mode
        return {
            "approved": True,
            "issues": [],
            "score": 1.0
        }

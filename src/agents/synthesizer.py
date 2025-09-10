from typing import Dict, Any
from .base_agent import BaseAgent
from loguru import logger

class SynthesizerAgent(BaseAgent):
    """Agent to synthesize final answers from retrieved information (mocked)"""

    def __init__(self):
        super().__init__(
            name="Synthesizer",
            description="Combines retrieved documents to generate answers"
        )
        logger.info("Synthesizer Agent initialized (mock)")

    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        retrieved_info = task.get('retrieved_info', {})
        original_query = task.get('original_query', '')

        # Aggregate all text from retrieved documents
        documents_texts = []
        for sub_query_key, data in retrieved_info.items():
            docs = data.get("results", [])
            for doc in docs:
                documents_texts.append(doc.get('content', ''))

        if not documents_texts:
            # Mocked no info fallback
            response = f"No relevant information found for the query: {original_query}"
        else:
            # For mock, join snippets and add a canned response
            combined = " ".join(documents_texts[:3])
            response = f"Synthesized answer (mock): {combined}"

        logger.info("Mock synthesis completed")
        return {
            "response": response
        }

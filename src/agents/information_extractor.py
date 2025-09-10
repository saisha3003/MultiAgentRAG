from typing import Dict, Any, List
from .base_agent import BaseAgent
from utils.vector_store import VectorStoreManager
from loguru import logger

class InformationExtractionAgent(BaseAgent):
    """Agent responsible for retrieving information relevant to the query"""

    def __init__(self, knowledge_collections: List[str]):
        super().__init__(
            name="InfoExtractor",
            description="Retrieves relevant documents and data from knowledge collections"
        )
        self.vector_store_manager = VectorStoreManager()
        self.knowledge_collections = knowledge_collections
        logger.info(f"Information Extraction Agent initialized with sources: {knowledge_collections}")

    async def process(self, task: Dict[str, Any]) -> Dict[str, Any]:
        queries = task.get('queries', [])
        if not queries:
            raise ValueError("No queries provided for information extraction")

        retrieved_info = {}
        for idx, query in enumerate(queries):
            all_results = []
            logger.info(f"Retrieving info for sub-query {idx + 1}: {query}")
            for collection_name in self.knowledge_collections:
                try:
                    results = self.vector_store_manager.query(collection_name, query, n_results=5)
                    logger.info(f"Found {len(results)} results in collection: {collection_name}")
                    all_results.extend(results)
                except Exception as e:
                    logger.error(f"Retrieval failed in collection {collection_name}: {str(e)}")
            retrieved_info[f"query_{idx}"] = {
                "query": query,
                "results": all_results
            }

        return {
            "retrieved_information": retrieved_info
        }

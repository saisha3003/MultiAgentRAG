import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from orchestrator.master_orchestrator import MasterOrchestrator
from utils.logging_config import setup_logging

async def test_master_orchestrator():
    logger = setup_logging()

    # Replace with your actual knowledge collections names
    knowledge_collections = ["my_documents"]

    orchestrator = MasterOrchestrator(knowledge_collections)

    test_queries = [
        "What is artificial intelligence?",
        "Explain effects of climate change."
    ]

    for query in test_queries:
        print(f"\nProcessing query: {query}")
        result = await orchestrator.run_pipeline(query)
        print("Answer:\n", result["answer"])
        print("QA Passed:", result["quality_assurance"].get("approved", False))

if __name__ == "__main__":
    asyncio.run(test_master_orchestrator())

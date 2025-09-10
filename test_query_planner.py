import asyncio
import sys
import os

# Add src folder to sys.path so imports work
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agents.query_planner import QueryPlanningAgent
from utils.logging_config import setup_logging

async def test_query_planner():
    logger = setup_logging()
    planner = QueryPlanningAgent()

    test_queries = [
        "What is the capital of France?",
        "Compare economic growth of USA and China over the last decade",
        "Analyze impact of climate change on agriculture in Africa"
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: {query}")
        try:
            result = await planner.process({'query': query})
            print("Result:", result)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    asyncio.run(test_query_planner())

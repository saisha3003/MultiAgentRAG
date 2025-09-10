import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agents.quality_assurance import QualityAssuranceAgent
from utils.logging_config import setup_logging

async def test_quality_assurance():
    logger = setup_logging()
    qa_agent = QualityAssuranceAgent()

    sample_response = (
        "Artificial intelligence refers to the simulation of human intelligence "
        "in machines that are programmed to think like humans and mimic their actions."
    )
    original_query = "What is artificial intelligence?"
    source_info = {
        "query_0": {
            "results": [
                {"content": "AI is the field of computer science that simulates intelligence."}
            ]
        }
    }

    result = await qa_agent.process({
        "response": sample_response,
        "original_query": original_query,
        "source_info": source_info
    })

    print("\nQuality Assurance Result:", result)

if __name__ == "__main__":
    asyncio.run(test_quality_assurance())

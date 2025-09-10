from typing import Dict, Any, List
import asyncio
from loguru import logger
from agents.query_planner import QueryPlanningAgent
from agents.information_extractor import InformationExtractionAgent
from agents.synthesizer import SynthesizerAgent
from agents.quality_assurance import QualityAssuranceAgent

class MasterOrchestrator:
    """Coordinates multi-agent RAG workflow"""

    def __init__(self, knowledge_collections: List[str]):
        self.query_planner = QueryPlanningAgent()
        self.info_extractor = InformationExtractionAgent(knowledge_collections)
        self.synthesizer = SynthesizerAgent()
        self.qa_agent = QualityAssuranceAgent()

    async def run_pipeline(self, user_query: str) -> Dict[str, Any]:
        logger.info("Starting query pipeline")

        plan_result = await self.query_planner.process({"query": user_query})
        sub_queries = plan_result.get("sub_queries") or [user_query]

        extraction_result = await self.info_extractor.process({"queries": sub_queries})

        synthesis_result = await self.synthesizer.process({
            "retrieved_info": extraction_result.get("retrieved_information", {}),
            "original_query": user_query
        })

        answer = synthesis_result.get("response", "")

        qa_result = await self.qa_agent.process({
            "response": answer,
            "original_query": user_query,
            "source_info": extraction_result.get("retrieved_information", {})
        })

        logger.info(f"Pipeline completed. QA Approved: {qa_result.get('approved', False)}")

        return {
            "query_plan": plan_result,
            "retrieved_info": extraction_result,
            "answer": answer,
            "quality_assurance": qa_result
        }

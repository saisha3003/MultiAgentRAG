# Multi-Agent Retrieval-Augmented Generation (RAG) System

A modular Python framework that integrates multiple AI agents to retrieve relevant information from documents and generate coherent answers to user queries. Includes components for query planning, information extraction, answer synthesis, and quality assurance, exposed via a FastAPI REST API. Mock implementations allow local testing without API costs.

---

## Features

- **Multi-Agent Architecture** – Separate agents for query planning, information extraction, synthesis, and quality assurance.  
- **Local Vector Database** – Uses ChromaDB to store and retrieve document embeddings.  
- **Mock Embeddings & LLMs** – Zero-vector embeddings and canned responses enable offline development.  
- **FastAPI Service** – Simple `/query` endpoint for JSON requests and `/health` for status checks.  

---

## Getting Started

### Prerequisites

- Python 3.11+  
- Git  

### Installation

1. **Clone the repository**  
git clone https://github.com/your-username/MultiAgentRAG.git
cd MultiAgentRAG

2. **Create & activate a virtual environment**  
python -m venv venv

Windows
venv\Scripts\activate

macOS/Linux
source venv/bin/activate

3. **Install dependencies**  
pip install -r requirements.txt

---

## Setup

1. **Populate the vector store**  
Adds sample documents to ChromaDB using mock embeddings:  
python populate_vector_store.py

2. **Verify data**  
Ensure `data/chroma_db/` directory contains your Chroma collections.

---

## Running the API

Start the FastAPI server with Uvicorn:

uvicorn app:app --reload


- The service listens on `http://127.0.0.1:8000`.

---

## API Usage

### Health Check

- **Endpoint:** `GET /health`  
- **Response:**  
{ "status": "ok" }


### Query Endpoint

- **Endpoint:** `POST /query`  
- **Request Body:**  
{
"query": "Your question here"
}- 
**Response Body:**  
{
"answer": "Synthesized answer (mock): ...",
"qa_passed": true
}

**Example using curl (Windows CMD):**

curl -X POST http://127.0.0.1:8000/query -H "Content-Type: application/json" -d "{"query":"What is artificial intelligence?"}"

---

## Project Structure

MultiAgentRAG/
├── app.py
├── populate_vector_store.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│ └── chroma_db/
├── src/
│ ├── orchestrator/
│ │ └── master_orchestrator.py
│ ├── agents/
│ │ ├── base_agent.py
│ │ ├── query_planner.py
│ │ ├── information_extractor.py
│ │ ├── synthesizer.py
│ │ └── quality_assurance.py
│ └── utils/
│ ├── config.py
│ ├── logging_config.py
│ └── vector_store.py

---

## Customization

- **Real Embeddings & LLMs** – Replace `MockEmbeddings` with `OpenAIEmbeddings` and remove mock logic in agents.  
- **Additional Collections** – Call `VectorStoreManager.create_collection(...)` for more document sets.  
- **Agent Logic** – Update `process` methods in agents for custom planning, retrieval, or synthesis behavior. 

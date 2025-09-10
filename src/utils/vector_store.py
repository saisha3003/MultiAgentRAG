import os
from typing import List, Dict
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from loguru import logger
from .config import settings
import numpy as np

class MockEmbeddings:
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [np.zeros(1536).tolist() for _ in texts]
    def embed_query(self, text: str) -> List[float]:
        return np.zeros(1536).tolist()

class VectorStoreManager:
    """Manage Chroma vector store with mock embeddings (no API calls)"""

    def __init__(self):
        os.makedirs(settings.chroma_persist_directory, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_directory,
            settings=ChromaSettings(allow_reset=True),
        )
        # Preload existing collections into the local cache
        self.collections = {}
        for col in self.client.list_collections():
            try:
                collection = self.client.get_collection(name=col.name)
                self.collections[col.name] = collection
                logger.info(f"Preloaded existing collection: {col.name}")
            except Exception as e:
                logger.warning(f"Failed to preload {col.name}: {e}")

        self.embeddings = MockEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        logger.info(f"Initialized ChromaDB at {settings.chroma_persist_directory}")

    def create_collection(self, collection_name: str):
        if collection_name in self.collections:
            logger.info(f"Collection {collection_name} exists, retrieving it.")
            return self.collections[collection_name]
        try:
            collection = self.client.create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
            self.collections[collection_name] = collection
            logger.info(f"Created collection: {collection_name}")
            return collection
        except Exception as e:
            logger.error(f"Failed to create collection {collection_name}: {e}")
            raise

    def add_documents(self, collection_name: str, documents: List[str], metadatas: List[Dict] = None):
        if collection_name not in self.collections:
            self.create_collection(collection_name)
        col = self.collections[collection_name]

        split_texts = []
        for doc in documents:
            split_texts.extend(self.text_splitter.split_text(doc))

        embeddings = self.embeddings.embed_documents(split_texts)
        ids = [f"doc_{i}" for i in range(len(split_texts))]
        meta = metadatas or [{"source": f"doc_{i}", "chunk_id": i} for i in range(len(split_texts))]

        try:
            col.add(
                documents=split_texts,
                embeddings=embeddings,
                metadatas=meta,
                ids=ids,
            )
            logger.info(f"Added {len(split_texts)} chunks to {collection_name}")
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise

    def query(self, collection_name: str, query_text: str, n_results: int = 5):
        if collection_name not in self.collections:
            logger.warning(f"Collection {collection_name} does not exist")
            return []

        col = self.collections[collection_name]
        query_emb = self.embeddings.embed_query(query_text)
        results = col.query(query_embeddings=[query_emb], n_results=n_results)

        formatted = []
        for i in range(len(results["documents"][0])):
            formatted.append({
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "similarity_score": 1 - results["distances"][0][i],
                "id": results["ids"][0][i],
            })
        return formatted

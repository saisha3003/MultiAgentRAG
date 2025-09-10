from src.utils.vector_store import VectorStoreManager

def populate_sample_data():
    documents = [
        "Artificial intelligence is the simulation of human intelligence in machines.",
        "Climate change refers to significant shifts in global or regional climates.",
        "Machine learning is a subset of AI focusing on learning patterns from data."
    ]
    vs_manager = VectorStoreManager()
    vs_manager.create_collection("my_documents")
    vs_manager.add_documents("my_documents", documents)

if __name__ == "__main__":
    populate_sample_data()

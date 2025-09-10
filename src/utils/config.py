import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    project_name: str = os.getenv("PROJECT_NAME", "MultiAgentRAG")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    max_tokens: int = int(os.getenv("MAX_TOKENS", "4000"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))
    chroma_persist_directory: str = os.getenv("CHROMA_PERSIST_DIRECTORY", "./data/chroma_db")

settings = Settings()

def validate_config():
    if not settings.openai_api_key:
        print("Warning: OPENAI_API_KEY is empty. Using mock implementations.")
    print(f"Config loaded: {settings.project_name}, log level {settings.log_level}")

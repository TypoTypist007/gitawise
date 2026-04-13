import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_ENVIRONMENT: str = os.getenv("PINECONE_ENVIRONMENT", "")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "gita-700-verses")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o")
    API_TITLE: str = "GitaWise API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    class Config:
        env_file = ".env"

settings = Settings()

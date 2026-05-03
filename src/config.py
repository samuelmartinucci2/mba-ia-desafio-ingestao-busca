import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    OPENAI_CHAT_MODEL: str = "gpt-4o-mini"
    
    GOOGLE_API_KEY: Optional[str] = None
    GOOGLE_EMBEDDING_MODEL: str = "models/gemini-embedding-001"
    GOOGLE_CHAT_MODEL: str = "models/gemini-flash-latest"
    
    # Database
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/rag"
    PG_VECTOR_COLLECTION_NAME: str = "pdf_chunks"
    
    # Files
    PDF_PATH: str = "document.pdf"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Instância global para ser importada
settings = Settings()

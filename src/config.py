import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pydantic import computed_field

class Settings(BaseSettings):
    # API Keys
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    OPENAI_CHAT_MODEL: str = "gpt-4o-mini"
    
    GOOGLE_API_KEY: Optional[str] = None
    GOOGLE_EMBEDDING_MODEL: str = "models/gemini-embedding-001"
    GOOGLE_CHAT_MODEL: str = "models/gemini-flash-latest"
    
    # Database (Mandatory fields - application will fail if not provided in .env)
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    
    # Optional full URL (overrides individual fields if provided)
    DB_URL_OVERRIDE: Optional[str] = None
    
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        if self.DB_URL_OVERRIDE:
            return self.DB_URL_OVERRIDE
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    PG_VECTOR_COLLECTION_NAME: str = "pdf_chunks"
    
    # Files
    PDF_PATH: str = "document.pdf"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Instância global para ser importada
settings = Settings()

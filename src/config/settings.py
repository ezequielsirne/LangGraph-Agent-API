from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    pinecone_api_key: str = Field(..., env="PINECONE_API_KEY")
    pinecone_index_name: str = Field("langgraph-agent-api", env="PINECONE_INDEX_NAME")
    pinecone_environment: str = Field("us-east-1", env="PINECONE_ENVIRONMENT")
    embedding_model: str = "text-embedding-3-small"
    booking_api_user: str = Field(..., env="BOOKING_API_USER")
    booking_api_pass: str = Field(..., env="BOOKING_API_PASS")
    booking_api_url: str = Field(..., env="BOOKING_API_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instancia global de settings que podés importar en cualquier módulo
settings = Settings()

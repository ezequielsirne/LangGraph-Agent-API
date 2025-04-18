from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    model: str = Field(..., env="MODEL")
    pinecone_api_key: str = Field(..., env="PINECONE_API_KEY")
    pinecone_index_name: str = Field("langgraph-agent-api", env="PINECONE_INDEX_NAME")
    pinecone_environment: str = Field("us-east-1", env="PINECONE_ENVIRONMENT")
    embedding_model: str = "text-embedding-3-small"
    booking_api_user: str = Field(..., env="BOOKING_API_USER")
    booking_api_pass: str = Field(..., env="BOOKING_API_PASS")
    booking_api_url: str = Field(..., env="BOOKING_API_URL")
    langsmith_tracing: bool = Field(False, env="LANGSMITH_TRACING")
    langsmith_endpoint: str = Field(None, env="LANGSMITH_ENDPOINT")
    langsmith_api_key: str = Field(None, env="LANGSMITH_API_KEY")
    langsmith_project: str = Field(None, env="LANGSMITH_PROJECT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

# Instancia global de settings que podés importar en cualquier módulo
settings = Settings()

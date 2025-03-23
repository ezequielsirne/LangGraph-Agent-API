from pinecone import Pinecone, ServerlessSpec
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain_openai import OpenAIEmbeddings
from src.config.settings import settings  # Importamos la configuración centralizada

# Create Pinecone client using settings
pc = Pinecone(api_key=settings.pinecone_api_key)

# Index name from settings
index_name = settings.pinecone_index_name

# Check if index exists; if not, create it
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Connect to the existing index using the correct embedding model from settings
embedding_model = OpenAIEmbeddings(model=settings.embedding_model)
vector_db = LangchainPinecone.from_existing_index(index_name=index_name, embedding=embedding_model)

def add_documents_to_pinecone(documents):
    """Add documents to Pinecone."""
    vector_db.add_documents(documents)

def get_retriever():
    """Return the retriever for searching in Pinecone."""
    return vector_db.as_retriever()

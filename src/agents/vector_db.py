import os
import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar API Key y entorno de Pinecone
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENVIRONMENT"))

# Nombre del índice en Pinecone
index_name = os.getenv("PINECONE_INDEX_NAME", "langgraph-agent-api")

# Verificar si el índice ya existe, si no, crearlo
if index_name not in pinecone.list_indexes():
    pinecone.create_index(name=index_name, dimension=1536, metric="cosine")

# Conectar al índice existente
embedding_model = OpenAIEmbeddings()
vector_db = Pinecone.from_existing_index(index_name=index_name, embedding=embedding_model)

def add_documents_to_pinecone(documents):
    """ Agrega documentos a Pinecone. """
    vector_db.add_documents(documents)

def get_retriever():
    """ Retorna el retriever para búsqueda en Pinecone. """
    return vector_db.as_retriever()

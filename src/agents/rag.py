from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from src.agents.vector_db import add_documents_to_pinecone

def load_documents():
    """Carga la información del hotel y la almacena en Pinecone."""
    loader = TextLoader("data/hotel_info.txt")
    documents = loader.load()

    # Dividir en fragmentos pequeños para embeddings eficientes
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # Agregar documentos a Pinecone
    add_documents_to_pinecone(texts)

# Cargar documentos si Pinecone está vacío
load_documents()

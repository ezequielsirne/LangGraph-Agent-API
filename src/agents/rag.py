from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from src.agents.vector_db import add_documents_to_pinecone
from src.config.settings import settings 
import pinecone

def load_pdf_into_pinecone(pdf_path: str, chunk_size: int, chunk_overlap: int):
    """Loads a PDF, splits it into chunks with specified parameters, uploads them to Pinecone, and displays a summary."""
    # Connect to Pinecone using settings
    pc = pinecone.Pinecone(api_key=settings.pinecone_api_key)
    index_name = settings.pinecone_index_name
    index = pc.Index(index_name)

    # Check current index state before uploading
    stats_before = index.describe_index_stats()
    previous_vectors = stats_before['total_vector_count']
    if previous_vectors > 0:
        print(f"The index '{index_name}' already contains {previous_vectors} vectors.")
    else:
        print(f"The index '{index_name}' is empty, proceeding to upload data.")

    # Process the PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_documents(documents)

    # Upload documents to Pinecone
    add_documents_to_pinecone(texts)
    print(f"PDF '{pdf_path}' successfully uploaded. {len(texts)} text chunks added.")

    # Check index state after upload
    stats_after = index.describe_index_stats()
    new_total = stats_after['total_vector_count']
    added_vectors = new_total - previous_vectors

    print(f"\nOperation summary:")
    print(f"- Vectors before upload: {previous_vectors}")
    print(f"- Vectors added: {added_vectors}")
    print(f"- Total vectors in index now: {new_total}")

    # Display preview of the first uploaded chunk
    if texts:
        first_chunk = texts[0]
        print("\nFirst uploaded chunk:")
        print(f"Content (truncated): {first_chunk.page_content[:200]}...")
        print(f"Metadata: {first_chunk.metadata}")

if __name__ == "__main__":
    load_pdf_into_pinecone("data/RAG.pdf", chunk_size=500, chunk_overlap=50)

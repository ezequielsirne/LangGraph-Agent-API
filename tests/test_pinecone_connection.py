import os
from pinecone import Pinecone
from dotenv import load_dotenv

def test_pinecone_connection():
    # Cargar variables de entorno
    load_dotenv()

    # Crear instancia de Pinecone
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    # Listar índices disponibles
    indexes = pc.list_indexes().names()
    print("Índices disponibles:", indexes)

    # Verificar conexión al índice
    index_name = os.getenv("PINECONE_INDEX_NAME")
    if index_name in indexes:
        print(f"Conectado a Pinecone: {index_name}")
    else:
        print("Error: Índice no encontrado")


if __name__ == "__main__":
    test_pinecone_connection()

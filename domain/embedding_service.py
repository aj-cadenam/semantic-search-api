# domain/embedding_service.py
from adapters.openai_adapter import (
    generate_embedding,
)  # Importa la función para generar embeddings
from adapters.database import (
    insert_embedding,
    get_similar_embeddings,
)  # Importa las funciones de la base de datos


# Función para almacenar un embedding en la base de datos
def store_embedding(prompt):
    embedding_vector = generate_embedding(prompt)  # Genera el embedding usando OpenAI
    insert_embedding(prompt, embedding_vector)  # Lo almacena en PostgreSQL
    return embedding_vector


# Función para encontrar textos similares con base en embeddings
def find_similar_texts(prompt):
    embedding_vector = generate_embedding(prompt)  # Genera el embedding del prompt
    return get_similar_embeddings(
        embedding_vector
    )  # Busca los textos más similares en la base de datos

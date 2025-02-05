# domain/embedding_service.py


from adapters.openai_adapter import generate_embedding
from adapters.database import insert_embedding, get_similar_embeddings


def store_embedding(prompt):
    embedding_vector = generate_embedding(prompt)
    insert_embedding(prompt, embedding_vector)
    return embedding_vector


def find_similar_texts(prompt):
    embedding_vector = generate_embedding(prompt)
    return get_similar_embeddings(embedding_vector)

import psycopg2
from config.config import DB_PARAMS


def connect_db():
    return psycopg2.connect(**DB_PARAMS)


def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS vector_table (
            id bigserial PRIMARY KEY,
            keyword VARCHAR(100),
            embedding vector(1536)
        );
        """
    )
    cursor.execute(
        "CREATE INDEX ON vector_table USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);"
    )
    conn.commit()
    cursor.close()
    conn.close()


def insert_embedding(keyword, embedding_vector):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO vector_table (keyword, embedding) VALUES (%s, %s::vector)",
        (keyword, embedding_vector),
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_similar_embeddings(embedding_vector):
    formatted_embedding = f"[{','.join(map(str, embedding_vector))}]"
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT keyword, 1 - (embedding <=> %s::vector) AS similarity
        FROM vector_table
        WHERE 1 - (embedding <=> %s::vector) >= 0.5
        ORDER BY embedding <=> %s::vector
        LIMIT 5;
        """,
        (formatted_embedding, formatted_embedding, formatted_embedding),
    )
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [result[0] for result in results]

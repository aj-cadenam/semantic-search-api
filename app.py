from flask import Flask, render_template, request
import os
from openai import OpenAI

import numpy as np
import json
import psycopg2
from psycopg2.extras import execute_values
from psycopg2.extras import Json
import numpy as np


api_key = os.getenv("OPENAI_API_KEY")  # Obtiene la clave de las variables de entorno
if not api_key:
    raise ValueError("La variable de entorno OPENAI_API_KEY no está configurada")

client = OpenAI(api_key=api_key)

app = Flask(__name__)

# Configurar la clave de API de OpenAI (asegúrate de que la clave está configurada en las variables de entorno)

DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "1234",
    "host": "class-pgvector",
    "port": "5432",
}


def connect_db():
    return psycopg2.connect(**DB_PARAMS)


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    # Habilitar la extensión vector si no está habilitada
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS vector_table (id bigserial PRIMARY KEY, keyword VARCHAR(100), embedding vector(1536));
        
        """
    )
    # Crear un índice para optimizar búsquedas de similitud con `pgvector`
    cursor.execute(
        "CREATE INDEX ON vector_table USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);"
    )

    conn.commit()
    cursor.close()
    conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_embedding", methods=["POST"])
def get_embedding():
    """
    Ruta que recibe un mensaje del usuario, genera su embedding y almacena el embedding en PostgreSQL.
    """

    # Extraer el texto ingresado por el usuario en el formulario
    prompt = request.form["prompt"] or request.form["predefined_prompt"]

    # Generar el embedding utilizando la API de OpenAI
    embedding_response = client.embeddings.create(
        model="text-embedding-ada-002", input=prompt
    )

    # Extraer el embedding del resultado de la API
    embedding_vector = embedding_response.data[0].embedding

    # Almacenar el embedding en PostgreSQL
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
       
        INSERT INTO vector_table (keyword, embedding) VALUES (%s, %s::vector)
        """,
        (prompt, embedding_vector),
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(embedding_vector)
    return render_template("index.html", embedding=json.dumps(embedding_vector))


@app.route("/get_similar", methods=["POST"])
def get_similar():
    """
    Ruta que recibe un mensaje del usuario, genera su embedding y busca mensajes similares en PostgreSQL.
    """
    # Extraer el texto ingresado por el usuario en el formulario
    prompt = request.form["prompt"] or request.form["predefined_prompt"]

    # Generar el embedding utilizando la API de OpenAI
    embedding_response = client.embeddings.create(
        model="text-embedding-ada-002", input=prompt
    )

    # Extraer el embedding del resultado de la API
    embedding_vector = embedding_response.data[0].embedding
    formatted_embedding = f"({','.join(map(str, embedding_vector))})"

    # Buscar mensajes similares en PostgreSQL
    conn = connect_db()
    cursor = conn.cursor()
    # Convertir el embedding a formato PostgreSQL

    formatted_embedding = f"[{','.join(map(str, embedding_vector))}]"

    cursor.execute(
        """
        SELECT keyword, 1 - (embedding <=> %s::vector) AS similarity
        FROM vector_table
        WHERE 1 - (embedding <=> %s::vector) >= 0.5
        ORDER BY embedding <=> %s::vector
        LIMIT 5;
        """,
        (
            formatted_embedding,
            formatted_embedding,
            formatted_embedding,
        ),  # ✅ Pasar 3 valores correctos
    )
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    # Extraer los textos de los resultados
    similar_texts = [result[0] for result in results]
    print(similar_texts)
    return render_template("index.html", similar_texts=similar_texts)


if __name__ == "__main__":
    create_table()
    app.run(debug=True, host="0.0.0.0", port=5000)

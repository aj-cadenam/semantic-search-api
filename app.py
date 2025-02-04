from flask import Flask, render_template, request
import os
from openai import OpenAI
import numpy as np
import json
import psycopg2
from psycopg2.extras import execute_values
from psycopg2.extras import Json
import numpy as np

# Get the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("The environment variable OPENAI_API_KEY is not set")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Initialize Flask application
app = Flask(__name__)

# Database connection parameters
DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "1234",
    "host": "class-pgvector",
    "port": "5432",
}


# Function to establish a database connection
def connect_db():
    return psycopg2.connect(**DB_PARAMS)


# Function to create the table in PostgreSQL
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    # Enable the vector extension if not already enabled
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # Create the table if it does not exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS vector_table (
            id bigserial PRIMARY KEY,
            keyword VARCHAR(100),
            embedding vector(1536)
        );
        """
    )

    # Create an index to optimize similarity searches using pgvector
    cursor.execute(
        "CREATE INDEX ON vector_table USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);"
    )

    conn.commit()
    cursor.close()
    conn.close()


# Define the home route
@app.route("/")
def index():
    return render_template("index.html")


# Route to generate and store embeddings
@app.route("/get_embedding", methods=["POST"])
def get_embedding():
    """
    Route that receives user input, generates its embedding, and stores the embedding in PostgreSQL.
    """
    # Retrieve the user input from the form
    prompt = request.form["prompt"] or request.form["predefined_prompt"]

    # Generate the embedding using OpenAI API
    embedding_response = client.embeddings.create(
        model="text-embedding-ada-002", input=prompt
    )

    # Extract the embedding from the API response
    embedding_vector = embedding_response.data[0].embedding

    # Store the embedding in PostgreSQL
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

    print(embedding_vector)  # Print the embedding for debugging purposes
    return render_template("index.html", embedding=json.dumps(embedding_vector))


# Route to find similar texts based on embeddings
@app.route("/get_similar", methods=["POST"])
def get_similar():
    """
    Route that receives user input, generates its embedding, and searches for similar messages in PostgreSQL.
    """
    # Retrieve the user input from the form
    prompt = request.form["prompt"] or request.form["predefined_prompt"]

    # Generate the embedding using OpenAI API
    embedding_response = client.embeddings.create(
        model="text-embedding-ada-002", input=prompt
    )

    # Extract the embedding from the API response
    embedding_vector = embedding_response.data[0].embedding
    formatted_embedding = f"({','.join(map(str, embedding_vector))})"

    # Search for similar messages in PostgreSQL
    conn = connect_db()
    cursor = conn.cursor()

    # Convert the embedding into PostgreSQL format
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
        ),  # ✅ Pass the correct 3 values
    )
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    # Extract the text results from the query output
    similar_texts = [result[0] for result in results]
    print(similar_texts)  # Print similar texts for debugging purposes
    return render_template("index.html", similar_texts=similar_texts)


# Run the Flask app
if __name__ == "__main__":
    create_table()  # Ensure the table is created before starting the server
    app.run(debug=True, host="0.0.0.0", port=5000)

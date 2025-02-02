from flask import Flask, render_template, request
from openai import OpenAI

client = OpenAI(api_key="xxx")
import numpy as np
import json
import psycopg2
from psycopg2.extras import Json

app = Flask(__name__)

# Configurar la clave de API de OpenAI (asegúrate de que la clave está configurada en las variables de entorno)

# Configurar la conexión a la base de datos PostgreSQL
DB_PARAMS = {
    "dbname": "tu_base_de_datos",
    "user": "tu_usuario",
    "password": "tu_contraseña",
    "host": "localhost",
    "port": "5432",
}


def connect_db():
    return psycopg2.connect(**DB_PARAMS)


@app.route("/")
def index():
    return render_template("./index.html")


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
        INSERT INTO embeddings (text, embedding)
        VALUES (%s, %s)
        """,
        (prompt, Json(embedding_vector)),
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(embedding_vector)
    return render_template("index.html", embedding=json.dumps(embedding_vector))


if __name__ == "__main__":
    app.run(debug=True)

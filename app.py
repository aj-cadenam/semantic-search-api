# app.py
from flask import Flask, render_template, request
from domain.embedding_service import (
    store_embedding,
    find_similar_texts,
)  # Importa la lógica de embeddings
from adapters.database import (
    create_table,
)  # Importa la función para crear la tabla en PostgreSQL

# Inicializa la aplicación Flask
app = Flask(
    __name__, template_folder="templates"
)  # Asegura que busca las plantillas en la carpeta correcta


# Ruta principal: muestra la página de inicio
@app.route("/")
def index():
    return render_template("index.html")  # Flask buscará en /templates/index.html


# Ruta para obtener y almacenar embeddings
@app.route("/get_embedding", methods=["POST"])
def get_embedding():
    prompt = (
        request.form["prompt"] or request.form["predefined_prompt"]
    )  # Obtiene el texto ingresado
    embedding_vector = store_embedding(prompt)  # Genera y almacena el embedding
    return render_template(
        "index.html", embedding=embedding_vector
    )  # Muestra el resultado


# Ruta para buscar textos similares con embeddings
@app.route("/get_similar", methods=["POST"])
def get_similar():
    prompt = (
        request.form["prompt"] or request.form["predefined_prompt"]
    )  # Obtiene el texto ingresado
    similar_texts = find_similar_texts(prompt)  # Encuentra textos similares en la BD
    return render_template(
        "index.html", similar_texts=similar_texts
    )  # Muestra los textos similares en la página


# Punto de entrada principal
if __name__ == "__main__":
    create_table()  # Asegura que la tabla esté creada antes de iniciar el servidor
    app.run(debug=True, host="0.0.0.0", port=5000)  # Inicia el servidor Flask

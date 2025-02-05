# app.py
from flask import Flask, render_template, request
from domain.embedding_service import store_embedding, find_similar_texts
from adapters.database import create_table

app = Flask(
    __name__, template_folder="templates"
)  # Asegurar que busca las plantillas en la carpeta correcta


@app.route("/")
def index():
    return render_template("index.html")  # Flask buscará en /templates/index.html


@app.route("/get_embedding", methods=["POST"])
def get_embedding():
    prompt = request.form["prompt"] or request.form["predefined_prompt"]
    embedding_vector = store_embedding(prompt)
    return render_template("index.html", embedding=embedding_vector)


@app.route("/get_similar", methods=["POST"])
def get_similar():
    prompt = request.form["prompt"] or request.form["predefined_prompt"]
    similar_texts = find_similar_texts(prompt)
    return render_template("index.html", similar_texts=similar_texts)


if __name__ == "__main__":
    create_table()  # Asegurar que la tabla está creada antes de iniciar el servidor
    app.run(debug=True, host="0.0.0.0", port=5000)

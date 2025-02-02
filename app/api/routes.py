from flask import Blueprint, request, jsonify
from app.core.services import TextService
from app.adapters.openai_adapter import OpenAIAdapter
from app.infrastructure.repository import TextRepository

bp = Blueprint("texts", __name__)

text_service = TextService(repository=TextRepository(), ai_adapter=OpenAIAdapter())


@bp.route("/texts/", methods=["POST"])
def add_text():
    data = request.json
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "El texto no puede estar vacío"}), 400

    text_id = text_service.add_text(text)
    return jsonify({"message": "Texto almacenado", "id": text_id}), 201


@bp.route("/texts/search", methods=["GET"])
def search_texts():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "El query no puede estar vacío"}), 400

    results = text_service.search_similar_texts(query)
    return jsonify(results)

from flask import Blueprint, render_template, request
from app.adapters.openai_adapter import OpenAIAdapter

web_bp = Blueprint("web", __name__)

ai_adapter = OpenAIAdapter()


@web_bp.route("/")
def index():
    return render_template("index.html")


@web_bp.route("/get_prompt", methods=["POST"])
def get_prompt():
    prompt = request.form.get("prompt") or request.form.get("predefined_prompt")

    if not prompt:
        return render_template("index.html", result="Error: Prompt vacío.")

    result = ai_adapter.chat_with_gpt(prompt)
    return render_template("index.html", result=result)

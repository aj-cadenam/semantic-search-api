import openai
import os


class OpenAIAdapter:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY no está configurada en el entorno.")
        openai.api_key = "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"

    def get_embedding(self, text: str):
        """Obtiene el embedding de un texto usando OpenAI text-embedding-ada-002."""
        response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
        return response["data"][0]["embedding"]

    def chat_with_gpt(self, prompt: str):
        """Genera una respuesta con GPT-4 basado en un prompt de usuario."""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )
        return response["choices"][0]["message"]["content"].strip()

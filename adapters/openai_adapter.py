# adapters/openai_adapter.py


from openai import OpenAI
from config.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_embedding(prompt):
    response = client.embeddings.create(model="text-embedding-ada-002", input=prompt)
    return response.data[0].embedding

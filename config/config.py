# config/config.py
import os

# Configuración de la API de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("The environment variable OPENAI_API_KEY is not set")

# Configuración de la base de datos PostgreSQL
DB_PARAMS = {
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "1234"),
    "host": os.getenv("DB_HOST", "class-pgvector"),  # Cambia si usas Docker
    "port": os.getenv("DB_PORT", "5432"),
}

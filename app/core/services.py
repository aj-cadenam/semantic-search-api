from app.adapters.openai_adapter import OpenAIAdapter
from app.infrastructure.repository import TextRepository
from app.core.entities import TextEntity


class TextService:
    def __init__(self, repository: TextRepository, ai_adapter: OpenAIAdapter):
        self.repository = repository
        self.ai_adapter = ai_adapter

    def add_text(self, text: str):
        """Genera el embedding y guarda el texto en la base de datos."""
        embedding = self.ai_adapter.get_embedding(text)
        text_entity = TextEntity(id=None, text=text, embedding=embedding)
        return self.repository.save_text(text_entity)

    def search_similar_texts(self, query: str):
        """Busca textos más similares usando embeddings."""
        query_embedding = self.ai_adapter.get_embedding(query)
        return self.repository.search_by_embedding(query_embedding)

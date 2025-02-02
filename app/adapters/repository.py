from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from app.infrastructure.database import SessionLocal
from app.core.entities import TextEntity
from app.models import TextEntry


class TextRepository:
    def __init__(self, db: Session = SessionLocal()):
        self.db = db

    def save_text(self, text_entity: TextEntity):
        """Guarda un texto y su embedding en la base de datos."""
        new_text = TextEntry(text=text_entity.text, embedding=text_entity.embedding)
        self.db.add(new_text)
        self.db.commit()
        self.db.refresh(new_text)
        return new_text.id

    def search_by_embedding(self, query_embedding):
        """Encuentra los textos más similares por embeddings."""
        sql_query = text(
            "SELECT text, embedding <-> :query_embedding AS distance "
            "FROM texts ORDER BY distance LIMIT 5"
        )

        results = self.db.execute(
            sql_query, {"query_embedding": query_embedding}
        ).fetchall()
        return [{"text": row[0], "similarity": row[1]} for row in results]

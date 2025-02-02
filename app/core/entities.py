from dataclasses import dataclass
from typing import List


@dataclass
class TextEntity:
    id: int
    text: str
    embedding: List[float]

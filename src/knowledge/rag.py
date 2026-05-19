from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.knowledge.loader import KnowledgeDocument


DEFAULT_TOP_K = 3
DEFAULT_MIN_SCORE = 0.08


@dataclass(frozen=True)
class RetrievedDocument:
    title: str
    excerpt: str
    score: float
    source_path: str
    source_filename: str
    chunk_index: int


class RAGPipeline:
    def __init__(
        self,
        documents: list[KnowledgeDocument],
        vectorizer: TfidfVectorizer,
        matrix: Any,
        min_score: float = DEFAULT_MIN_SCORE,
    ) -> None:
        self.documents = documents
        self.vectorizer = vectorizer
        self.matrix = matrix
        self.min_score = min_score

    @classmethod
    def from_documents(
        cls,
        documents: list[KnowledgeDocument],
        min_score: float = DEFAULT_MIN_SCORE,
    ) -> "RAGPipeline":
        corpus = [document.content for document in documents] or [
            "Industria 4.0 dados automacao inteligencia artificial carreira"
        ]
        vectorizer = TfidfVectorizer(stop_words=None, ngram_range=(1, 2))
        matrix = vectorizer.fit_transform(corpus)
        return cls(documents, vectorizer, matrix, min_score=min_score)

    def retrieve(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K,
        min_score: float | None = None,
    ) -> list[RetrievedDocument]:
        if not self.documents or not query.strip():
            return []

        threshold = self.min_score if min_score is None else min_score
        query_matrix = self.vectorizer.transform([query])
        scores = cosine_similarity(query_matrix, self.matrix).flatten()
        ranked_indexes = scores.argsort()[::-1]

        results: list[RetrievedDocument] = []
        for index in ranked_indexes:
            score = float(scores[index])
            if score < threshold:
                continue
            document = self.documents[index]
            results.append(
                RetrievedDocument(
                    title=document.title,
                    excerpt=excerpt(document.content),
                    score=round(score, 4),
                    source_path=document.source_path,
                    source_filename=document.source_filename,
                    chunk_index=document.chunk_index,
                )
            )
            if len(results) >= top_k:
                break
        return results


def excerpt(content: str, limit: int = 420) -> str:
    normalized = " ".join(content.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3].rstrip() + "..."

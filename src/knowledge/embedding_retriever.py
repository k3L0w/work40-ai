from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import numpy as np

from src.knowledge.loader import KnowledgeDocument
from src.knowledge.rag import DEFAULT_MIN_SCORE, DEFAULT_TOP_K, RAGPipeline, RetrievedDocument, excerpt


logger = logging.getLogger(__name__)

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_EMBEDDING_CACHE = Path("data/.cache/embeddings.json")
EmbeddingMode = Literal["Auto", "TF-IDF", "Embeddings"]


class EmbeddingRetrievalError(RuntimeError):
    """Raised when embedding retrieval cannot be completed safely."""


@dataclass(frozen=True)
class EmbeddingCacheItem:
    embedding: list[float]
    content_hash: str
    source_path: str
    chunk_index: int


class EmbeddingRetriever:
    def __init__(
        self,
        documents: list[KnowledgeDocument],
        api_key: str,
        embedding_model: str = DEFAULT_EMBEDDING_MODEL,
        cache_path: Path = DEFAULT_EMBEDDING_CACHE,
        min_score: float = DEFAULT_MIN_SCORE,
    ) -> None:
        self.documents = documents
        self.api_key = api_key
        self.embedding_model = embedding_model
        self.cache_path = cache_path
        self.min_score = min_score
        self.retrieval_mode = "Embeddings"
        self._cache: dict[str, EmbeddingCacheItem] | None = None

    def retrieve(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K,
        min_score: float | None = None,
    ) -> list[RetrievedDocument]:
        if not self.documents or not query.strip():
            return []

        threshold = self.min_score if min_score is None else min_score
        document_embeddings = self._document_embeddings()
        query_embedding = np.array(self._embed_texts([query])[0], dtype=float)
        matrix = np.array(document_embeddings, dtype=float)
        scores = cosine_similarity(query_embedding, matrix)
        ranked_indexes = scores.argsort()[::-1]

        results: list[RetrievedDocument] = []
        for index in ranked_indexes:
            score = float(scores[index])
            if score < threshold:
                continue
            document = self.documents[int(index)]
            results.append(
                RetrievedDocument(
                    title=document.title,
                    excerpt=excerpt(document.content),
                    score=round(score, 4),
                    source_path=document.source_path,
                    source_filename=document.source_filename,
                    chunk_index=document.chunk_index,
                    category=document.category,
                    source_type=document.source_type,
                    last_reviewed=document.last_reviewed,
                )
            )
            if len(results) >= top_k:
                break
        return results

    def _document_embeddings(self) -> list[list[float]]:
        cache = self._load_cache()
        missing_documents = [
            document for document in self.documents if self._cache_key(document) not in cache
        ]
        if missing_documents:
            embeddings = self._embed_texts([document.content for document in missing_documents])
            for document, embedding in zip(missing_documents, embeddings, strict=True):
                cache[self._cache_key(document)] = EmbeddingCacheItem(
                    embedding=embedding,
                    content_hash=content_hash(document.content),
                    source_path=document.source_path,
                    chunk_index=document.chunk_index,
                )
            self._write_cache(cache)
        return [cache[self._cache_key(document)].embedding for document in self.documents]

    def _embed_texts(self, texts: list[str]) -> list[list[float]]:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key)
            response = client.embeddings.create(
                model=self.embedding_model,
                input=texts,
            )
        except Exception as exc:
            raise EmbeddingRetrievalError(str(exc)) from exc
        return [list(item.embedding) for item in response.data]

    def _load_cache(self) -> dict[str, EmbeddingCacheItem]:
        if self._cache is not None:
            return self._cache
        if not self.cache_path.exists():
            self._cache = {}
            return self._cache
        try:
            payload = json.loads(self.cache_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Embedding cache could not be read; rebuilding cache: %s", exc)
            self._cache = {}
            return self._cache
        if payload.get("embedding_model") != self.embedding_model:
            self._cache = {}
            return self._cache
        items = payload.get("items", {})
        self._cache = {
            key: EmbeddingCacheItem(
                embedding=list(value["embedding"]),
                content_hash=str(value["content_hash"]),
                source_path=str(value["source_path"]),
                chunk_index=int(value["chunk_index"]),
            )
            for key, value in items.items()
            if isinstance(value, dict) and "embedding" in value
        }
        return self._cache

    def _write_cache(self, cache: dict[str, EmbeddingCacheItem]) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "embedding_model": self.embedding_model,
            "items": {
                key: {
                    "embedding": item.embedding,
                    "content_hash": item.content_hash,
                    "source_path": item.source_path,
                    "chunk_index": item.chunk_index,
                }
                for key, item in cache.items()
            },
        }
        self.cache_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _cache_key(self, document: KnowledgeDocument) -> str:
        return "|".join(
            [
                self.embedding_model,
                document.source_path,
                str(document.chunk_index),
                content_hash(document.content),
            ]
        )


class RetrievalRouter:
    def __init__(
        self,
        tfidf_retriever: RAGPipeline,
        mode: EmbeddingMode,
        openai_api_key: str | None,
        embedding_model: str = DEFAULT_EMBEDDING_MODEL,
        cache_path: Path = DEFAULT_EMBEDDING_CACHE,
    ) -> None:
        self.tfidf_retriever = tfidf_retriever
        self.mode = mode
        self.openai_api_key = openai_api_key
        self.embedding_model = embedding_model
        self.cache_path = cache_path
        self.last_retrieval_mode = "TF-IDF"

    def retrieve(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K,
        min_score: float | None = None,
    ) -> list[RetrievedDocument]:
        if self.mode == "TF-IDF" or not self.openai_api_key:
            self.last_retrieval_mode = "TF-IDF"
            return self.tfidf_retriever.retrieve(query, top_k=top_k, min_score=min_score)

        try:
            embedding_retriever = EmbeddingRetriever(
                documents=self.tfidf_retriever.documents,
                api_key=self.openai_api_key,
                embedding_model=self.embedding_model,
                cache_path=self.cache_path,
                min_score=self.tfidf_retriever.min_score,
            )
            results = embedding_retriever.retrieve(query, top_k=top_k, min_score=min_score)
            self.last_retrieval_mode = "Embeddings"
            return results
        except EmbeddingRetrievalError as exc:
            logger.warning(
                "Embedding retrieval failed; falling back to TF-IDF retrieval: %s",
                exc,
            )
            self.last_retrieval_mode = "TF-IDF"
            return self.tfidf_retriever.retrieve(query, top_k=top_k, min_score=min_score)


def cosine_similarity(query_embedding: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    query_norm = np.linalg.norm(query_embedding)
    matrix_norms = np.linalg.norm(matrix, axis=1)
    denominator = matrix_norms * query_norm
    denominator = np.where(denominator == 0, 1e-12, denominator)
    return matrix.dot(query_embedding) / denominator


def content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

import json
import sys
from types import SimpleNamespace

from src.knowledge.embedding_retriever import EmbeddingRetriever, RetrievalRouter
from src.knowledge.loader import KnowledgeDocument
from src.knowledge.rag import RAGPipeline


class _FakeEmbeddings:
    def create(self, model: str, input: list[str]) -> object:
        return SimpleNamespace(
            data=[SimpleNamespace(embedding=_fake_embedding(text)) for text in input]
        )


class _FakeOpenAIClient:
    def __init__(self, api_key: str | None) -> None:
        self.embeddings = _FakeEmbeddings()


class _FailingEmbeddings:
    def create(self, model: str, input: list[str]) -> object:
        raise RuntimeError("embedding service unavailable")


class _FailingOpenAIClient:
    def __init__(self, api_key: str | None) -> None:
        self.embeddings = _FailingEmbeddings()


def test_router_uses_tfidf_when_no_api_key() -> None:
    tfidf = RAGPipeline.from_documents(_documents(), min_score=0.0)
    router = RetrievalRouter(
        tfidf_retriever=tfidf,
        mode="Auto",
        openai_api_key=None,
    )

    results = router.retrieve("alpha automation", top_k=1)

    assert results
    assert router.last_retrieval_mode == "TF-IDF"
    assert router.last_safe_error_type is None
    assert router.last_safe_error_message is None


def test_embedding_retriever_uses_mocked_embeddings_and_writes_cache(
    tmp_path,
    monkeypatch,
) -> None:
    monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=_FakeOpenAIClient))
    cache_path = tmp_path / "embeddings.json"
    retriever = EmbeddingRetriever(
        documents=_documents(),
        api_key="test-key",
        cache_path=cache_path,
        min_score=0.0,
    )

    results = retriever.retrieve("alpha", top_k=1)

    assert results[0].source_filename == "alpha.md"
    assert cache_path.exists()
    payload = json.loads(cache_path.read_text(encoding="utf-8"))
    assert payload["embedding_model"] == "text-embedding-3-small"
    assert len(payload["items"]) == 2


def test_embedding_retriever_reads_existing_cache(tmp_path, monkeypatch) -> None:
    monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=_FakeOpenAIClient))
    cache_path = tmp_path / "embeddings.json"
    first = EmbeddingRetriever(
        documents=_documents(),
        api_key="test-key",
        cache_path=cache_path,
        min_score=0.0,
    )
    first.retrieve("alpha", top_k=1)

    second = EmbeddingRetriever(
        documents=_documents(),
        api_key="test-key",
        cache_path=cache_path,
        min_score=0.0,
    )
    results = second.retrieve("beta", top_k=1)

    assert results[0].source_filename == "beta.md"
    assert cache_path.exists()


def test_router_auto_uses_embeddings_when_available(tmp_path, monkeypatch) -> None:
    monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=_FakeOpenAIClient))
    tfidf = RAGPipeline.from_documents(_documents(), min_score=0.0)
    router = RetrievalRouter(
        tfidf_retriever=tfidf,
        mode="Auto",
        openai_api_key="test-key",
        cache_path=tmp_path / "embeddings.json",
    )

    results = router.retrieve("beta", top_k=1)

    assert results[0].source_filename == "beta.md"
    assert router.last_retrieval_mode == "Embeddings"
    assert router.last_safe_error_type is None
    assert router.last_safe_error_message is None


def test_embedding_failure_falls_back_to_tfidf(tmp_path, monkeypatch) -> None:
    monkeypatch.setitem(
        sys.modules,
        "openai",
        SimpleNamespace(OpenAI=_FailingOpenAIClient),
    )
    tfidf = RAGPipeline.from_documents(_documents(), min_score=0.0)
    router = RetrievalRouter(
        tfidf_retriever=tfidf,
        mode="Embeddings",
        openai_api_key="test-key",
        cache_path=tmp_path / "embeddings.json",
    )

    results = router.retrieve("alpha automation", top_k=1)

    assert results
    assert router.last_retrieval_mode == "TF-IDF"
    assert router.last_safe_error_type == "RuntimeError"
    assert router.last_safe_error_message is not None
    assert "test-key" not in router.last_safe_error_message


def _documents() -> list[KnowledgeDocument]:
    return [
        KnowledgeDocument(
            title="Alpha",
            content="alpha automation process data",
            source_path="data/knowledge/test/alpha.md",
            source_filename="alpha.md",
            chunk_index=0,
            category="test",
        ),
        KnowledgeDocument(
            title="Beta",
            content="beta robotics maintenance sensors",
            source_path="data/knowledge/test/beta.md",
            source_filename="beta.md",
            chunk_index=0,
            category="test",
        ),
    ]


def _fake_embedding(text: str) -> list[float]:
    lowered = text.lower()
    if "alpha" in lowered:
        return [1.0, 0.0]
    if "beta" in lowered:
        return [0.0, 1.0]
    return [0.5, 0.5]

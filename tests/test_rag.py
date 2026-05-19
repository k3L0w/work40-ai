from pathlib import Path

from src.ai.assistant import LOW_CONFIDENCE_ANSWER, answer_question
from src.knowledge.loader import load_documents, split_markdown_text
from src.knowledge.rag import RAGPipeline
from src.utils.config import Settings


def test_load_documents_reads_markdown_with_metadata() -> None:
    docs = load_documents(Path("data/knowledge"), chunk_size=180, chunk_overlap=30)

    assert docs
    assert docs[0].title
    assert docs[0].source_filename.endswith(".md")
    assert docs[0].chunk_index >= 0


def test_splitter_uses_overlap_and_skips_empty_chunks() -> None:
    content = "# Title\n\n" + "automacao " * 80

    chunks = split_markdown_text(content, chunk_size=120, chunk_overlap=20)

    assert len(chunks) > 1
    assert all(chunk.strip() for chunk in chunks)
    assert chunks[0][-20:] == chunks[1][:20]


def test_rag_retrieves_relevant_document_with_scores() -> None:
    docs = load_documents(Path("data/knowledge"))
    rag = RAGPipeline.from_documents(docs, min_score=0.05)

    results = rag.retrieve("automacao de tarefas repetitivas", top_k=2)

    assert results
    assert len(results) <= 2
    assert results[0].score > 0
    assert any("automation.md" == result.source_filename for result in results)
    assert all(result.chunk_index >= 0 for result in results)


def test_retriever_filters_low_confidence_queries() -> None:
    docs = load_documents(Path("data/knowledge"))
    rag = RAGPipeline.from_documents(docs, min_score=0.2)

    results = rag.retrieve("culinaria medieval e astronomia nautica", top_k=3)

    assert results == []


def test_assistant_uses_offline_fallback_without_key() -> None:
    docs = load_documents(Path("data/knowledge"))
    rag = RAGPipeline.from_documents(docs)
    settings = Settings(openai_api_key=None, openai_model="test", app_env="test")

    response = answer_question("Como estudar IA?", rag, settings)

    assert response.used_model == "offline-fallback"
    assert "Resposta offline deterministica" in response.answer
    assert response.sources


def test_assistant_reports_low_confidence_without_sources() -> None:
    docs = load_documents(Path("data/knowledge"))
    rag = RAGPipeline.from_documents(docs, min_score=0.2)
    settings = Settings(openai_api_key=None, openai_model="test", app_env="test")

    response = answer_question("culinaria medieval e astronomia nautica", rag, settings)

    assert response.answer == LOW_CONFIDENCE_ANSWER
    assert response.sources == []

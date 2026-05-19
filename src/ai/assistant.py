from __future__ import annotations

from dataclasses import dataclass

from src.knowledge.rag import RAGPipeline, RetrievedDocument
from src.utils.config import Settings


LOW_CONFIDENCE_ANSWER = (
    "Nao tenho informacoes suficientes na base de conhecimento local para responder "
    "com confianca. Adicione fontes relevantes em data/knowledge/ ou reformule a "
    "pergunta dentro do escopo de Industria 4.0, competencias, automacao e carreira."
)


@dataclass(frozen=True)
class AssistantResponse:
    answer: str
    sources: list[RetrievedDocument]
    used_model: str


def answer_question(
    question: str,
    rag: RAGPipeline,
    settings: Settings,
    top_k: int = 3,
) -> AssistantResponse:
    sources = rag.retrieve(question, top_k=top_k)
    if not sources:
        return AssistantResponse(
            answer=LOW_CONFIDENCE_ANSWER,
            sources=[],
            used_model="offline-fallback",
        )

    if settings.openai_api_key:
        generated = _answer_with_openai(question, sources, settings)
        if generated:
            return AssistantResponse(generated, sources, settings.openai_model)

    return AssistantResponse(
        answer=_offline_answer(question, sources),
        sources=sources,
        used_model="offline-fallback",
    )


def _offline_answer(question: str, sources: list[RetrievedDocument]) -> str:
    context = " ".join(source.excerpt for source in sources)
    return (
        "Resposta offline deterministica: para avancar na era da Industria 4.0, "
        "priorize uma combinacao de alfabetizacao em dados, automacao, IA aplicada "
        "e habilidades humanas como comunicacao e adaptabilidade. "
        f"Pergunta analisada: '{question}'. Evidencias recuperadas: {context}"
    )


def _answer_with_openai(
    question: str,
    sources: list[RetrievedDocument],
    settings: Settings,
) -> str | None:
    try:
        from openai import OpenAI
    except ImportError:
        return None

    client = OpenAI(api_key=settings.openai_api_key)
    context = "\n\n".join(
        "Fonte: "
        f"{source.title} ({source.source_filename}, chunk {source.chunk_index}, "
        f"score {source.score})\n{source.excerpt}"
        for source in sources
    )
    prompt = (
        "Voce e o Work4.0 AI, um assistente de carreira para Industria 4.0. "
        "Responda em portugues, seja pratico e use apenas o contexto quando "
        "possivel. Se o contexto nao sustentar a resposta, diga que nao ha "
        "informacao suficiente.\n\n"
        f"Contexto:\n{context}\n\nPergunta: {question}"
    )
    try:
        response = client.responses.create(
            model=settings.openai_model,
            input=prompt,
            temperature=0.2,
        )
    except Exception:
        return None
    return response.output_text

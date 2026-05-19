from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from src.knowledge.rag import DEFAULT_MIN_SCORE, RAGPipeline, RetrievedDocument
from src.utils.config import Settings


logger = logging.getLogger(__name__)

LOW_CONFIDENCE_ANSWER = (
    "Não encontrei informação suficiente na base de conhecimento para responder "
    "com precisão."
)

ANSWER_SECTIONS = (
    "Resposta direta",
    "Explicação",
    "Impacto no futuro do trabalho",
    "Competências recomendadas",
    "Próxima ação prática",
    "Fontes internas usadas",
)

SYSTEM_PROMPT = """
Você é o Work4.0 AI, um assistente de inteligência de carreira para a era da
Indústria 4.0.

Regras obrigatórias:
- Responda sempre em português brasileiro.
- Em modo RAG, responda somente com base no contexto recuperado.
- Cite as fontes internas usadas pelo título, arquivo e chunk.
- Não invente estatísticas, percentuais, pesquisas ou números.
- Não prometa emprego, promoção, recolocação ou salário.
- Não faça previsões absolutas sobre extinção de profissões.
- Recomende desenvolvimento prático de competências.
- Adapte a resposta ao perfil selecionado pelo usuário.
- Se o contexto recuperado for insuficiente, responda exatamente:
  "Não encontrei informação suficiente na base de conhecimento para responder
  com precisão."

Formato obrigatório quando houver contexto suficiente:
Resposta direta
Explicação
Impacto no futuro do trabalho
Competências recomendadas
Próxima ação prática
Fontes internas usadas
Limitação da resposta, quando necessário
""".strip()


@dataclass(frozen=True)
class AssistantResponse:
    answer: str
    sources: list[RetrievedDocument]
    used_model: str
    ai_mode: str
    warning: str | None = None


def answer_question(
    question: str,
    rag: RAGPipeline,
    settings: Settings,
    user_profile: dict[str, Any] | None = None,
    top_k: int = 3,
    min_retrieval_score: float = DEFAULT_MIN_SCORE,
) -> AssistantResponse:
    sources = rag.retrieve(question, top_k=top_k)
    if not _has_sufficient_context(sources, min_retrieval_score):
        return AssistantResponse(
            answer=LOW_CONFIDENCE_ANSWER,
            sources=[],
            used_model="offline-fallback",
            ai_mode="offline",
        )

    if settings.openai_api_key:
        generated = _answer_with_openai(question, sources, settings, user_profile)
        if generated:
            return AssistantResponse(
                answer=generated,
                sources=sources,
                used_model=settings.openai_model,
                ai_mode="online",
            )
        return AssistantResponse(
            answer=_offline_answer(question, sources, user_profile),
            sources=sources,
            used_model="offline-fallback",
            ai_mode="fallback",
            warning=(
                "A IA online não pôde ser usada neste momento. "
                "O sistema respondeu com o modo offline."
            ),
        )

    return AssistantResponse(
        answer=_offline_answer(question, sources, user_profile),
        sources=sources,
        used_model="offline-fallback",
        ai_mode="offline",
    )


def _has_sufficient_context(
    sources: list[RetrievedDocument],
    min_retrieval_score: float,
) -> bool:
    if not sources:
        return False
    return max(source.score for source in sources) >= min_retrieval_score


def _offline_answer(
    question: str,
    sources: list[RetrievedDocument],
    user_profile: dict[str, Any] | None,
) -> str:
    profile_note = _profile_note(user_profile)
    source_summary = _summarize_sources(sources)
    citations = _format_sources(sources)
    recommended_skills = _recommended_skills_from_sources(sources)
    practical_action = _practical_action_from_sources(sources)
    future_impact = _future_impact_from_sources(sources)
    limitation = (
        "\n\nLimitação da resposta\n"
        "Esta resposta usa apenas a base interna recuperada e não inclui dados "
        "externos, estatísticas de mercado ou garantias de empregabilidade."
    )
    return (
        "Resposta direta\n"
        f"{profile_note}com base nos trechos recuperados, a preparação deve "
        "priorizar as competências e ações citadas nas fontes internas usadas "
        "abaixo.\n\n"
        "Explicação\n"
        f"Para a pergunta \"{question}\", os trechos recuperados destacam: "
        f"{source_summary}\n\n"
        "Impacto no futuro do trabalho\n"
        f"{future_impact}\n\n"
        "Competências recomendadas\n"
        f"{recommended_skills}\n\n"
        "Próxima ação prática\n"
        f"{practical_action}\n\n"
        "Fontes internas usadas\n"
        f"{citations}"
        f"{limitation}"
    )


def _answer_with_openai(
    question: str,
    sources: list[RetrievedDocument],
    settings: Settings,
    user_profile: dict[str, Any] | None,
) -> str | None:
    try:
        from openai import OpenAI
    except ImportError as exc:
        logger.warning("OpenAI SDK is not installed; using offline fallback: %s", exc)
        return None

    try:
        client = OpenAI(api_key=settings.openai_api_key)
    except Exception as exc:
        logger.warning("OpenAI client initialization failed; using offline fallback: %s", exc)
        return None

    context = "\n\n".join(
        "Fonte: "
        f"{source.title} ({source.source_filename}, chunk {source.chunk_index}, "
        f"score {source.score})\n{source.excerpt}"
        for source in sources
    )
    profile = _format_profile(user_profile)
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Perfil selecionado:\n{profile}\n\n"
        f"Contexto recuperado:\n{context}\n\n"
        f"Pergunta: {question}"
    )
    try:
        response = client.responses.create(
            model=settings.openai_model,
            input=prompt,
            temperature=0.2,
        )
    except Exception as exc:
        logger.warning("OpenAI response generation failed; using offline fallback: %s", exc)
        return None
    return response.output_text


def _profile_note(user_profile: dict[str, Any] | None) -> str:
    if not user_profile:
        return ""
    role = str(user_profile.get("role") or "").strip()
    goal = str(user_profile.get("career_goal") or "").strip()
    current_role = str(user_profile.get("current_role") or "").strip()
    parts = []
    if role:
        parts.append(f"para o perfil {role}")
    if current_role:
        parts.append(f"na área atual de {current_role}")
    if goal:
        parts.append(f"com objetivo de {goal}")
    if not parts:
        return ""
    return ", ".join(parts) + ", "


def _format_profile(user_profile: dict[str, Any] | None) -> str:
    if not user_profile:
        return "Perfil não informado."
    fields = {
        "perfil": user_profile.get("role"),
        "objetivo": user_profile.get("career_goal"),
        "área atual": user_profile.get("current_role"),
        "horas semanais": user_profile.get("weekly_hours"),
        "competências atuais": user_profile.get("selected_skills"),
    }
    return "\n".join(
        f"- {label}: {value}" for label, value in fields.items() if value
    ) or "Perfil não informado."


def _summarize_sources(sources: list[RetrievedDocument]) -> str:
    snippets = []
    for source in sources:
        clean_excerpt = source.excerpt.rstrip(".")
        snippets.append(f"{clean_excerpt} [{_source_label(source)}]")
    return " ".join(snippets)


def _future_impact_from_sources(sources: list[RetrievedDocument]) -> str:
    source_text = " ".join(source.excerpt.lower() for source in sources)
    if "substituicao de tarefas" in source_text or "substituição de tarefas" in source_text:
        return (
            "Os trechos recuperados indicam que o impacto não é apenas substituição "
            "de tarefas: também envolve novas funções, aprendizado contínuo, uso de "
            "dados e colaboração com tecnologias."
        )
    if "tarefas repetitivas" in source_text or "previsiveis" in source_text:
        return (
            "Os trechos recuperados indicam maior exposição de tarefas repetitivas, "
            "previsíveis e baseadas em regras, sem afirmar extinção absoluta de "
            "profissões."
        )
    if "competencias" in source_text or "competências" in source_text:
        return (
            "Os trechos recuperados conectam o futuro do trabalho ao desenvolvimento "
            "contínuo de competências técnicas, humanas e éticas."
        )
    return (
        "Os trechos recuperados são limitados; por isso, a resposta evita previsões "
        "absolutas e se concentra no que a base interna citada sustenta."
    )


def _recommended_skills_from_sources(sources: list[RetrievedDocument]) -> str:
    source_text = " ".join(source.excerpt.lower() for source in sources)
    skill_terms = {
        "alfabetização em dados": ("alfabetizacao em dados", "dados"),
        "pensamento computacional": ("pensamento computacional",),
        "fundamentos de inteligência artificial": (
            "inteligencia artificial",
            "ia",
        ),
        "automação de processos": ("automacao",),
        "segurança digital": ("seguranca digital",),
        "comunicação": ("comunicacao",),
        "resolução de problemas": ("resolucao de problemas",),
        "gestão de mudança": ("gestao de mudanca",),
        "julgamento contextual": ("julgamento contextual",),
        "criatividade": ("criatividade",),
        "negociação": ("negociacao",),
    }
    found = [
        skill
        for skill, aliases in skill_terms.items()
        if any(alias in source_text for alias in aliases)
    ]
    if found:
        return "Priorize as competências citadas nas fontes recuperadas: " + ", ".join(
            found
        ) + "."
    return (
        "Os trechos recuperados não detalham uma lista ampla de competências; "
        "use apenas as capacidades explicitamente mencionadas nas fontes citadas."
    )


def _practical_action_from_sources(sources: list[RetrievedDocument]) -> str:
    source_text = " ".join(source.excerpt.lower() for source in sources)
    if "portfolio" in source_text:
        return (
            "Transforme uma prática aplicada em evidência de portfólio, combinando "
            "teoria curta, execução prática e reflexão sobre impacto ético."
        )
    if "tarefas repetitivas" in source_text or "automacao" in source_text:
        return (
            "Escolha uma tarefa repetitiva do seu contexto, descreva como ela é "
            "feita hoje e identifique quais ferramentas de automação poderiam "
            "apoiar o redesenho dessa atividade."
        )
    if "dados" in source_text:
        return (
            "Mapeie uma decisão do seu trabalho ou estudo que possa ser melhorada "
            "com dados e registre como comunicaria o resultado com clareza."
        )
    return (
        "Revise as fontes internas citadas e transforme um ponto recuperado em uma "
        "atividade prática pequena, observável e registrada."
    )


def _format_sources(sources: list[RetrievedDocument]) -> str:
    return "\n".join(
        f"- {_source_label(source)}: {source.title}" for source in sources
    )


def _source_label(source: RetrievedDocument) -> str:
    return f"{source.source_filename}#chunk-{source.chunk_index}"

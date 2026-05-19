from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ai.assistant import answer_question
from src.features.automation import simulate_automation_impact
from src.features.planning import build_plan, recommend_study_path
from src.features.readiness import calculate_readiness_score
from src.features.skills import diagnose_skills
from src.knowledge.loader import load_documents
from src.knowledge.rag import RAGPipeline
from src.ui.markdown_export import build_markdown_report
from src.utils.config import get_settings


st.set_page_config(
    page_title="Work4.0 AI",
    page_icon="W4",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource(show_spinner=False)
def get_rag_pipeline() -> RAGPipeline:
    docs = load_documents(ROOT / "data" / "knowledge")
    return RAGPipeline.from_documents(docs)


def render_header() -> None:
    st.title("Work4.0 AI")
    st.caption("Inteligencia de carreira para a era da Industria 4.0")


def render_sidebar() -> dict[str, object]:
    st.sidebar.header("Perfil")
    role = st.sidebar.selectbox(
        "Modo",
        ["Estudante", "Trabalhador", "Professor", "Empresa / RH"],
    )
    career_goal = st.sidebar.text_input(
        "Objetivo profissional",
        value="Analista de dados industriais",
    )
    current_role = st.sidebar.text_input("Cargo ou area atual", value="Operacoes")
    weekly_hours = st.sidebar.slider("Horas de estudo por semana", 1, 20, 6)
    selected_skills = st.sidebar.multiselect(
        "Competencias atuais",
        [
            "Python",
            "Dados",
            "Automacao",
            "IA generativa",
            "Robotica",
            "IoT",
            "Comunicacao",
            "Gestao de mudanca",
        ],
        default=["Dados", "Comunicacao"],
    )
    return {
        "role": role,
        "career_goal": career_goal,
        "current_role": current_role,
        "weekly_hours": weekly_hours,
        "selected_skills": selected_skills,
    }


def render_dashboard(profile: dict[str, object], rag: RAGPipeline) -> None:
    selected_skills = list(profile["selected_skills"])
    diagnosis = diagnose_skills(selected_skills, str(profile["career_goal"]))
    readiness = calculate_readiness_score(
        technical_skills=diagnosis.coverage_ratio,
        learning_hours_per_week=int(profile["weekly_hours"]),
        adaptability=0.72,
        collaboration=0.78 if "Comunicacao" in selected_skills else 0.58,
    )
    impact = simulate_automation_impact(str(profile["current_role"]), selected_skills)
    study_path = recommend_study_path(diagnosis.gaps, int(profile["weekly_hours"]))
    plan = build_plan(study_path, str(profile["career_goal"]))

    score_col, impact_col, gaps_col = st.columns(3)
    score_col.metric("Industry 4.0 Readiness", f"{readiness.score}/100")
    impact_col.metric("Impacto de automacao", impact.level)
    gaps_col.metric("Lacunas prioritarias", len(diagnosis.gaps))

    st.progress(readiness.score / 100)
    st.write(readiness.summary)

    tab_ai, tab_skills, tab_plan, tab_modes, tab_export = st.tabs(
        ["Assistente RAG", "Diagnostico", "Plano", "Modos", "Exportar"]
    )

    with tab_ai:
        question = st.text_area(
            "Pergunte sobre carreira, automacao, IA, robotica ou competencias",
            value="Como devo me preparar para a Industria 4.0?",
            height=100,
        )
        if st.button("Responder", type="primary"):
            settings = get_settings()
            response = answer_question(question, rag, settings, user_profile=profile)
            st.subheader("Resposta")
            st.write(response.answer)
            st.subheader("Fontes")
            if not response.sources:
                st.info("Nenhuma fonte relevante encontrada na base local.")
            for source in response.sources:
                st.markdown(
                    "- "
                    f"**{source.title}** | arquivo `{source.source_filename}` | "
                    f"chunk `{source.chunk_index}` | score `{source.score:.4f}`\n\n"
                    f"  {source.excerpt}"
                )

    with tab_skills:
        st.subheader("Diagnostico de competencias")
        st.write(diagnosis.summary)
        st.dataframe(
            pd.DataFrame(
                {
                    "Competencia": diagnosis.required_skills,
                    "Status": [
                        "Presente" if skill in selected_skills else "Priorizar"
                        for skill in diagnosis.required_skills
                    ],
                }
            ),
            use_container_width=True,
            hide_index=True,
        )
        st.subheader("Simulador de impacto")
        st.write(impact.summary)
        st.write("Acoes recomendadas:")
        for action in impact.recommended_actions:
            st.markdown(f"- {action}")

    with tab_plan:
        st.subheader("Trilha personalizada")
        for item in study_path:
            st.markdown(f"- **{item.skill}**: {item.recommendation}")
        st.subheader("Plano 30/60/90 dias")
        for phase, actions in plan.items():
            st.markdown(f"**{phase}**")
            for action in actions:
                st.markdown(f"- {action}")

    with tab_modes:
        if profile["role"] == "Professor":
            st.subheader("Teacher mode")
            st.write(
                "Use os gaps da turma para montar rubricas, estudos de caso e "
                "atividades praticas com IA, dados e automacao."
            )
        elif profile["role"] == "Empresa / RH":
            st.subheader("Company / HR mode")
            st.write(
                "Agrupe diagnosticos por funcao, priorize reskilling e monitore "
                "riscos de automacao com foco em mobilidade interna."
            )
        else:
            st.subheader("Modo individual")
            st.write(
                "Concentre-se nas competencias com maior impacto no objetivo "
                "profissional e execute o plano semanalmente."
            )

    with tab_export:
        report = build_markdown_report(
            profile=profile,
            diagnosis=diagnosis,
            readiness=readiness,
            impact=impact,
            study_path=study_path,
            plan=plan,
        )
        st.download_button(
            "Baixar relatorio Markdown",
            data=report,
            file_name="work40-ai-report.md",
            mime="text/markdown",
        )
        st.code(report, language="markdown")


def main() -> None:
    render_header()
    profile = render_sidebar()
    rag = get_rag_pipeline()
    render_dashboard(profile, rag)


if __name__ == "__main__":
    main()

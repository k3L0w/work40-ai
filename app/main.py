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
from src.features.dashboard import (
    build_dashboard_metrics,
    ensure_metrics_state,
    record_diagnosis,
    record_question_answered,
)
from src.features.modes import generate_company_hr_plan, generate_teacher_mode_plan
from src.features.planning import (
    build_personalized_study_path,
    build_plan,
    recommend_study_path,
)
from src.features.readiness import calculate_readiness_score
from src.features.skills import diagnose_skills
from src.knowledge.loader import load_documents
from src.knowledge.rag import RAGPipeline
from src.ui.markdown_export import build_markdown_report, build_section_markdown
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
    current_level = st.sidebar.selectbox(
        "Nivel atual",
        ["Inicial", "Basico", "Intermediario", "Avancado"],
    )
    digital_maturity = st.sidebar.selectbox(
        "Maturidade digital",
        ["Inicial", "Basico", "Intermediario", "Avancado"],
    )
    weekly_hours = st.sidebar.slider("Horas de estudo por semana", 1, 20, 6)
    timeframe_weeks = st.sidebar.slider("Prazo da trilha (semanas)", 4, 12, 6)
    selected_skills = st.sidebar.multiselect(
        "Competencias atuais",
        [
            "Alfabetizacao digital",
            "Python",
            "Dados",
            "Automacao",
            "IA generativa",
            "Robotica",
            "IoT",
            "GitHub/portfolio",
            "Comunicacao",
            "Adaptabilidade",
            "Gestao de mudanca",
        ],
        default=["Dados", "Comunicacao"],
    )
    main_tasks_text = st.sidebar.text_area(
        "Principais tarefas",
        value="preencher relatorio\nconferir dados\nresolver problemas operacionais",
        height=110,
    )
    return {
        "role": role,
        "career_goal": career_goal,
        "current_role": current_role,
        "current_level": current_level,
        "digital_maturity": digital_maturity,
        "weekly_hours": weekly_hours,
        "timeframe_weeks": timeframe_weeks,
        "selected_skills": selected_skills,
        "main_tasks": [line.strip() for line in main_tasks_text.splitlines() if line.strip()],
    }


def render_dashboard(profile: dict[str, object], rag: RAGPipeline) -> None:
    ensure_metrics_state(st.session_state)
    settings = get_settings()
    selected_skills = list(profile["selected_skills"])
    diagnosis = diagnose_skills(selected_skills, str(profile["career_goal"]))
    readiness = calculate_readiness_score(
        technical_skills=diagnosis.coverage_ratio,
        learning_hours_per_week=int(profile["weekly_hours"]),
        adaptability=0.78 if "Adaptabilidade" in selected_skills else 0.62,
        collaboration=0.78 if "Comunicacao" in selected_skills else 0.58,
    )
    impact = simulate_automation_impact(
        role=str(profile["current_role"]),
        skills=selected_skills,
        main_tasks=list(profile["main_tasks"]),
        digital_maturity=str(profile["digital_maturity"]),
    )
    study_path = recommend_study_path(
        diagnosis.priority_skills or diagnosis.gaps,
        int(profile["weekly_hours"]),
        user_profile=str(profile["role"]),
        current_level=str(profile["current_level"]),
        goal=str(profile["career_goal"]),
        timeframe_weeks=int(profile["timeframe_weeks"]),
    )
    personalized_path = build_personalized_study_path(
        user_profile=str(profile["role"]),
        current_level=str(profile["current_level"]),
        goal=str(profile["career_goal"]),
        available_hours_per_week=int(profile["weekly_hours"]),
        timeframe_weeks=int(profile["timeframe_weeks"]),
        gaps=diagnosis.priority_skills or diagnosis.gaps,
    )
    plan = build_plan(study_path, str(profile["career_goal"]), str(profile["role"]))
    ai_mode = "online" if settings.openai_api_key else "offline"
    metrics = build_dashboard_metrics(st.session_state, str(profile["role"]), ai_mode)

    score_col, impact_col, gaps_col, mode_col = st.columns(4)
    score_col.metric("Work4.0 Score", f"{readiness.score}/100")
    impact_col.metric("Impacto de automacao", impact.level)
    gaps_col.metric("Prioridades", len(diagnosis.priority_skills))
    mode_col.metric("Modo IA", ai_mode)

    st.progress(readiness.score / 100)
    st.write(readiness.summary)

    metric_cols = st.columns(5)
    metric_cols[0].metric("Perguntas", metrics.questions_answered)
    metric_cols[1].metric("Diagnosticos", metrics.diagnoses_generated)
    metric_cols[2].metric("Media readiness", f"{metrics.average_readiness_score:.1f}")
    metric_cols[3].metric("Perfil", metrics.selected_profile)
    metric_cols[4].metric("Skills frequentes", len(metrics.most_recommended_skills))

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
            response = answer_question(question, rag, settings, user_profile=profile)
            record_question_answered(st.session_state)
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
        if st.button("Registrar diagnostico"):
            record_diagnosis(st.session_state, readiness.score, diagnosis.priority_skills)
            st.success("Diagnostico registrado nas metricas da sessao.")
        st.dataframe(
            pd.DataFrame(
                {
                    "Competencia": diagnosis.required_skills,
                    "Status": [
                        "Presente" if skill in diagnosis.strengths or skill in selected_skills else "Priorizar"
                        for skill in diagnosis.required_skills
                    ],
                }
            ),
            use_container_width=True,
            hide_index=True,
        )
        st.write("Proxima acao:", diagnosis.next_action)
        st.subheader("Scores de prontidao")
        st.dataframe(
            pd.DataFrame(
                [
                    ["Digital", readiness.digital_readiness_score],
                    ["IA", readiness.ai_readiness_score],
                    ["Automacao", readiness.automation_readiness_score],
                    ["Adaptabilidade", readiness.career_adaptability_score],
                    ["Geral Work4.0", readiness.general_work40_score],
                ],
                columns=["Dimensao", "Score"],
            ),
            use_container_width=True,
            hide_index=True,
        )
        st.subheader("Simulador de impacto")
        st.write(impact.summary)
        st.write(f"Oportunidade: {impact.opportunity_level}")
        st.write("Tarefas mais expostas:")
        for task in impact.tasks_more_likely_automated:
            st.markdown(f"- {task}")
        st.write("Tarefas com julgamento humano:")
        for task in impact.human_judgment_tasks:
            st.markdown(f"- {task}")
        st.write("Plano de adaptacao:")
        for action in impact.adaptation_plan:
            st.markdown(f"- {action}")

    with tab_plan:
        st.subheader("Trilha personalizada")
        st.write(personalized_path.portfolio_project_suggestion)
        for item in personalized_path.weekly_path:
            st.markdown(
                f"- **Semana {item.week} | {item.skill}**: {item.objective} "
                f"Entrega: {item.deliverable}."
            )
        st.subheader("Plano 30/60/90 dias")
        for phase, actions in plan.items():
            st.markdown(f"**{phase}**")
            for action in actions:
                st.markdown(f"- {action}")

    with tab_modes:
        if profile["role"] == "Professor":
            teacher_plan = generate_teacher_mode_plan(str(profile["career_goal"]))
            st.subheader("Teacher mode")
            st.write("Objetivos de aprendizagem:")
            for item in teacher_plan.learning_objectives:
                st.markdown(f"- {item}")
            st.write("Atividade:", teacher_plan.class_activity)
            st.write("Perguntas para debate:")
            for question in teacher_plan.debate_questions:
                st.markdown(f"- {question}")
            st.write("Projeto pratico:", teacher_plan.practical_project)
            st.write("Criterios de avaliacao:")
            for criterion in teacher_plan.evaluation_criteria:
                st.markdown(f"- {criterion}")
        elif profile["role"] == "Empresa / RH":
            hr_plan = generate_company_hr_plan(
                str(profile["current_role"]),
                str(profile["digital_maturity"]),
            )
            st.subheader("Company / HR mode")
            st.write(hr_plan.digital_maturity_diagnosis)
            st.write("Oportunidades de automacao:")
            for item in hr_plan.automation_opportunities:
                st.markdown(f"- {item}")
            st.write("Plano de treinamento:")
            for item in hr_plan.training_plan:
                st.markdown(f"- {item}")
            st.write("Indicadores de sucesso:")
            for item in hr_plan.success_indicators:
                st.markdown(f"- {item}")
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
        diagnosis_markdown = build_section_markdown(
            "Diagnostico Work4.0",
            [diagnosis.summary, diagnosis.next_action, *diagnosis.priority_skills],
        )
        st.download_button(
            "Baixar relatorio completo",
            data=report,
            file_name="work40-ai-report.md",
            mime="text/markdown",
        )
        st.download_button(
            "Baixar diagnostico",
            data=diagnosis_markdown,
            file_name="work40-ai-diagnostico.md",
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

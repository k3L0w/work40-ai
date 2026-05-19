from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.ai.assistant import LOW_CONFIDENCE_ANSWER, answer_question
from src.features.automation import AutomationImpact, simulate_automation_impact
from src.features.dashboard import (
    build_dashboard_metrics,
    ensure_metrics_state,
    record_diagnosis,
    record_question_answered,
)
from src.features.modes import CompanyHRPlan, TeacherModePlan
from src.features.modes import generate_company_hr_plan, generate_teacher_mode_plan
from src.features.planning import (
    PersonalizedStudyPath,
    StudyPathItem,
    build_personalized_study_path,
    build_plan,
    recommend_study_path,
)
from src.features.readiness import ReadinessScore, calculate_readiness_score
from src.features.skills import SkillDiagnosis, diagnose_skills
from src.knowledge.loader import load_documents
from src.knowledge.rag import RAGPipeline, RetrievedDocument
from src.ui.markdown_export import build_markdown_report, build_section_markdown
from src.utils.config import Settings, get_settings


st.set_page_config(
    page_title="Work4.0 AI",
    page_icon="W4",
    layout="wide",
    initial_sidebar_state="expanded",
)


EXAMPLE_QUESTIONS = [
    "Como devo me preparar para a Industria 4.0?",
    "Quais competencias devo priorizar para trabalhar com dados industriais?",
    "Como a automacao pode impactar tarefas repetitivas no meu cargo?",
]

SKILL_OPTIONS = [
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
]


@st.cache_resource(show_spinner=False)
def get_rag_pipeline() -> RAGPipeline:
    docs = load_documents(ROOT / "data" / "knowledge")
    return RAGPipeline.from_documents(docs)


def render_page_styles() -> None:
    st.markdown(
        """
        <style>
        .block-container {padding-top: 2rem; padding-bottom: 3rem;}
        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #d9e2ec;
            border-radius: 8px;
            padding: 14px 16px;
            color: #0f172a;
        }
        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #0f172a;
        }
        div[data-testid="stMetricLabel"] {font-weight: 650;}
        .w40-hero {
            border: 1px solid #d9e2ec;
            border-radius: 8px;
            padding: 30px 32px;
            background: linear-gradient(135deg, #f8fafc 0%, #eef6f3 100%);
            color: #0f172a;
            margin-bottom: 18px;
        }
        .w40-hero h1 {
            margin-bottom: 8px;
            color: #0f172a;
            letter-spacing: 0;
        }
        .w40-hero p {font-size: 1.02rem; color: #334155; max-width: 900px;}
        .w40-hero strong {color: #0f766e;}
        .w40-eyebrow {
            color: #0f766e;
            font-weight: 750;
            text-transform: uppercase;
            font-size: 0.78rem;
            margin-bottom: 8px;
        }
        .w40-section-note {color: #64748b; margin-top: -8px;}
        @media (prefers-color-scheme: dark) {
            div[data-testid="stMetric"] {
                background: #f8fafc;
                border-color: #cbd5e1;
            }
            .w40-hero {
                background: linear-gradient(135deg, #f8fafc 0%, #e6f4ef 100%);
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(profile: dict[str, object], ai_mode: str) -> None:
    st.markdown(
        f"""
        <section class="w40-hero">
            <div class="w40-eyebrow">MVP de inteligencia de carreira</div>
            <h1>Work4.0 AI</h1>
            <p>
                Diagnostico de competencias, prontidao para Industria 4.0,
                simulacao de impacto da automacao e planos praticos para
                estudantes, profissionais, professores e equipes de RH.
            </p>
            <p>
                Perfil ativo: <strong>{profile['role']}</strong> | IA:
                <strong>{ai_mode}</strong> | Objetivo:
                <strong>{profile['career_goal']}</strong>
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> dict[str, object]:
    st.sidebar.title("Configurar perfil")
    st.sidebar.caption("Ajuste os dados para personalizar diagnostico, plano e RAG.")
    role = st.sidebar.selectbox(
        "Perfil",
        ["Estudante", "Trabalhador", "Professor", "Empresa / RH"],
        help="Define o tom do plano e das recomendacoes.",
    )
    career_goal = st.sidebar.text_input(
        "Objetivo profissional",
        value="Analista de dados industriais",
        help="Exemplo: tecnico de automacao, analista de dados, professor de tecnologia.",
    )
    current_role = st.sidebar.text_input(
        "Cargo ou area atual",
        value="Operacoes",
        help="Use uma area real para melhorar o simulador de automacao.",
    )
    current_level = st.sidebar.selectbox(
        "Nivel atual",
        ["Inicial", "Basico", "Intermediario", "Avancado"],
    )
    digital_maturity = st.sidebar.selectbox(
        "Maturidade digital",
        ["Inicial", "Basico", "Intermediario", "Avancado"],
    )
    weekly_hours = st.sidebar.slider(
        "Horas de estudo por semana",
        1,
        20,
        6,
        help="Usado para definir ritmo e profundidade da trilha.",
    )
    timeframe_weeks = st.sidebar.slider("Prazo da trilha em semanas", 4, 12, 6)
    selected_skills = st.sidebar.multiselect(
        "Competencias atuais",
        SKILL_OPTIONS,
        default=["Dados", "Comunicacao"],
    )
    main_tasks_text = st.sidebar.text_area(
        "Principais tarefas",
        value="preencher relatorio\nconferir dados\nresolver problemas operacionais",
        height=120,
        help="Digite uma tarefa por linha para o simulador.",
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
        "main_tasks": [
            line.strip() for line in main_tasks_text.splitlines() if line.strip()
        ],
    }


def build_view_model(
    profile: dict[str, object], settings: Settings
) -> dict[str, Any]:
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
    teacher_plan = generate_teacher_mode_plan(str(profile["career_goal"]))
    hr_plan = generate_company_hr_plan(
        str(profile["current_role"]),
        str(profile["digital_maturity"]),
    )
    configured_mode = "online" if settings.openai_api_key else "offline"
    ai_mode = str(st.session_state.get("last_ai_mode", configured_mode))
    metrics = build_dashboard_metrics(st.session_state, str(profile["role"]), ai_mode)
    return {
        "diagnosis": diagnosis,
        "readiness": readiness,
        "impact": impact,
        "study_path": study_path,
        "personalized_path": personalized_path,
        "plan": plan,
        "teacher_plan": teacher_plan,
        "hr_plan": hr_plan,
        "ai_mode": ai_mode,
        "metrics": metrics,
    }


def render_key_metrics(
    readiness: ReadinessScore,
    impact: AutomationImpact,
    diagnosis: SkillDiagnosis,
    ai_mode: str,
) -> None:
    score_col, impact_col, priority_col, mode_col = st.columns(4)
    score_col.metric("Work4.0 Score", f"{readiness.score}/100")
    impact_col.metric("Risco de automacao", impact.risk_level)
    priority_col.metric("Skills prioritarias", len(diagnosis.priority_skills))
    mode_col.metric("Modo IA", ai_mode)
    st.progress(readiness.score / 100)
    st.caption(readiness.summary)


def render_overview(
    profile: dict[str, object],
    readiness: ReadinessScore,
    diagnosis: SkillDiagnosis,
    impact: AutomationImpact,
    personalized_path: PersonalizedStudyPath,
) -> None:
    st.header("Visao geral")
    st.markdown(
        '<p class="w40-section-note">Resumo executivo para orientar a proxima decisao.</p>',
        unsafe_allow_html=True,
    )
    left, right = st.columns([1.1, 0.9])
    with left.container(border=True):
        st.subheader("Prioridade do momento")
        st.write(diagnosis.next_action)
        st.write("Projeto sugerido:")
        st.info(personalized_path.portfolio_project_suggestion)
    with right.container(border=True):
        st.subheader("Contexto analisado")
        st.write(f"Perfil: {profile['role']}")
        st.write(f"Objetivo: {profile['career_goal']}")
        st.write(f"Area atual: {profile['current_role']}")
        st.write(f"Maturidade digital: {profile['digital_maturity']}")
    st.subheader("Leitura rapida")
    col_a, col_b, col_c = st.columns(3)
    render_list_card(col_a, "Pontos fortes", diagnosis.strengths)
    render_list_card(col_b, "Gaps principais", diagnosis.gaps[:5])
    render_list_card(col_c, "Plano de adaptacao", impact.adaptation_plan)
    st.subheader("Scores de prontidao")
    render_readiness_scores(readiness)


def render_assistant_tab(
    profile: dict[str, object], rag: RAGPipeline, settings: Settings
) -> None:
    st.header("Assistente RAG")
    st.caption("Respostas em portugues com fontes internas da base de conhecimento.")
    st.write("Perguntas exemplo")
    example_cols = st.columns(3)
    for index, question in enumerate(EXAMPLE_QUESTIONS):
        if example_cols[index].button(question, key=f"example_question_{index}"):
            st.session_state["rag_question"] = question
    st.session_state.setdefault("rag_question", EXAMPLE_QUESTIONS[0])
    st.text_area(
        "Sua pergunta",
        key="rag_question",
        height=120,
        help="Pergunte sobre carreira, automacao, IA, robotica ou competencias.",
    )
    ask_col, hint_col = st.columns([0.25, 0.75])
    if ask_col.button("Responder", type="primary", use_container_width=True):
        response = answer_question(
            str(st.session_state["rag_question"]),
            rag,
            settings,
            user_profile=profile,
        )
        record_question_answered(st.session_state)
        st.session_state["last_answer"] = response.answer
        st.session_state["last_sources"] = response.sources
        st.session_state["last_ai_mode"] = response.ai_mode
        st.session_state["last_ai_warning"] = response.warning
    hint_col.caption("Use perguntas especificas para obter citacoes mais precisas.")

    answer = st.session_state.get("last_answer")
    sources = st.session_state.get("last_sources", [])
    if answer:
        ai_mode = st.session_state.get("last_ai_mode", "offline")
        st.caption(f"Modo usado na ultima resposta: {ai_mode}")
        if st.session_state.get("last_ai_warning"):
            st.warning(str(st.session_state["last_ai_warning"]))
        if answer == LOW_CONFIDENCE_ANSWER:
            st.warning(
                "Nao encontrei contexto suficiente na base interna para responder "
                "com precisao. Tente reformular ou ampliar a base de conhecimento."
            )
        render_structured_answer(str(answer))
        render_sources(list(sources))


def render_structured_answer(answer: str) -> None:
    st.subheader("Resposta estruturada")
    sections = split_answer_sections(answer)
    if not sections:
        st.write(answer)
        return
    for title, content in sections.items():
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.write(content or "Sem conteudo adicional.")


def split_answer_sections(answer: str) -> dict[str, str]:
    section_titles = [
        "Resposta direta",
        "Explicação",
        "Impacto no futuro do trabalho",
        "Competências recomendadas",
        "Próxima ação prática",
        "Fontes internas usadas",
        "Limitação da resposta",
    ]
    lines = answer.splitlines()
    sections: dict[str, list[str]] = {}
    current_title = ""
    for line in lines:
        stripped = line.strip()
        if stripped in section_titles:
            current_title = stripped
            sections[current_title] = []
        elif current_title:
            sections[current_title].append(line)
    return {
        title: "\n".join(content).strip()
        for title, content in sections.items()
    }


def render_sources(sources: list[RetrievedDocument]) -> None:
    st.subheader("Fontes internas")
    if not sources:
        st.info("Nenhuma fonte relevante foi retornada para esta resposta.")
        return
    for source in sources:
        with st.container(border=True):
            meta_col, score_col = st.columns([0.75, 0.25])
            meta_col.markdown(f"**{source.title}**")
            meta_col.caption(
                f"Arquivo `{source.source_filename}` | chunk `{source.chunk_index}`"
            )
            score_col.metric("Score", f"{source.score:.4f}")
            st.write(source.excerpt)


def render_diagnosis_tab(
    diagnosis: SkillDiagnosis,
    readiness: ReadinessScore,
) -> None:
    st.header("Diagnostico")
    st.caption("Competencias atuais, lacunas e prontidao Work4.0.")
    if st.button("Registrar diagnostico", type="primary"):
        record_diagnosis(st.session_state, readiness.score, diagnosis.priority_skills)
        st.success("Diagnostico registrado nas metricas da sessao.")
    render_readiness_scores(readiness)
    col_a, col_b, col_c = st.columns(3)
    render_list_card(col_a, "Pontos fortes", diagnosis.strengths)
    render_list_card(col_b, "Lacunas", diagnosis.gaps)
    render_list_card(col_c, "Prioridades", diagnosis.priority_skills)
    with st.container(border=True):
        st.subheader("Proxima acao")
        st.write(diagnosis.next_action)
    st.subheader("Mapa de competencias")
    st.dataframe(
        pd.DataFrame(
            {
                "Competencia": diagnosis.required_skills,
                "Status": [
                    "Presente" if skill not in diagnosis.gaps else "Priorizar"
                    for skill in diagnosis.required_skills
                ],
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


def render_readiness_scores(readiness: ReadinessScore) -> None:
    score_data = pd.DataFrame(
        [
            ["Digital", readiness.digital_readiness_score],
            ["IA", readiness.ai_readiness_score],
            ["Automacao", readiness.automation_readiness_score],
            ["Adaptabilidade", readiness.career_adaptability_score],
            ["Geral Work4.0", readiness.general_work40_score],
        ],
        columns=["Dimensao", "Score"],
    )
    st.dataframe(score_data, use_container_width=True, hide_index=True)


def render_study_plan_tab(
    personalized_path: PersonalizedStudyPath,
    plan: dict[str, list[str]],
) -> None:
    st.header("Plano de estudos")
    st.caption("Trilha semanal, entregaveis praticos e plano 30/60/90 dias.")
    with st.container(border=True):
        st.subheader("Projeto de portfolio")
        st.write(personalized_path.portfolio_project_suggestion)
    st.subheader("Trilha semanal")
    for item in personalized_path.weekly_path:
        with st.container(border=True):
            st.markdown(f"**Semana {item.week}: {item.skill}**")
            st.write(f"Objetivo: {item.objective}")
            st.write(f"Entrega: {item.deliverable}")
            st.caption(item.recommendation)
    st.subheader("Plano 30/60/90")
    render_phase_plan(plan)


def render_automation_tab(
    profile: dict[str, object], selected_skills: list[str], default_impact: AutomationImpact
) -> None:
    st.header("Simulador de automacao")
    st.caption("Analise tarefas, risco, oportunidade e plano de adaptacao.")
    with st.form("automation_form"):
        sim_role = st.text_input("Cargo ou profissao", value=str(profile["current_role"]))
        sim_maturity = st.selectbox(
            "Maturidade digital",
            ["Inicial", "Basico", "Intermediario", "Avancado"],
            index=["Inicial", "Basico", "Intermediario", "Avancado"].index(
                str(profile["digital_maturity"])
            ),
        )
        sim_tasks = st.text_area(
            "Principais tarefas, uma por linha",
            value="\n".join(str(task) for task in profile["main_tasks"]),
            height=130,
        )
        submitted = st.form_submit_button("Simular impacto", type="primary")
    if submitted:
        impact = simulate_automation_impact(
            role=sim_role,
            skills=selected_skills,
            main_tasks=[line.strip() for line in sim_tasks.splitlines() if line.strip()],
            digital_maturity=sim_maturity,
        )
    else:
        impact = default_impact
    render_automation_result(impact)


def render_automation_result(impact: AutomationImpact) -> None:
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Risco", impact.risk_level)
    col_b.metric("Oportunidade", impact.opportunity_level)
    col_c.metric("Score de exposicao", f"{impact.score}/100")
    st.write(impact.summary)
    col_left, col_right = st.columns(2)
    render_list_card(col_left, "Tarefas mais expostas", impact.tasks_more_likely_automated)
    render_list_card(col_right, "Tarefas com julgamento humano", impact.human_judgment_tasks)
    render_list_card(st, "Plano de adaptacao", impact.adaptation_plan)


def render_teacher_mode_tab(teacher_plan: TeacherModePlan) -> None:
    st.header("Modo Professor")
    st.caption("Materiais para aula, debate, projeto pratico e avaliacao.")
    col_a, col_b = st.columns(2)
    render_list_card(col_a, "Plano de aula", teacher_plan.lesson_plan)
    render_list_card(col_b, "Objetivos de aprendizagem", teacher_plan.learning_objectives)
    with st.container(border=True):
        st.subheader("Atividade de sala")
        st.write(teacher_plan.class_activity)
    col_c, col_d = st.columns(2)
    render_list_card(col_c, "Perguntas para debate", teacher_plan.debate_questions)
    render_list_card(col_d, "Criterios de avaliacao", teacher_plan.evaluation_criteria)
    with st.container(border=True):
        st.subheader("Projeto pratico")
        st.write(teacher_plan.practical_project)


def render_company_mode_tab(hr_plan: CompanyHRPlan) -> None:
    st.header("Modo Empresa/RH")
    st.caption("Diagnostico de maturidade, oportunidades, riscos e roadmap.")
    with st.container(border=True):
        st.subheader("Diagnostico de maturidade")
        st.write(hr_plan.digital_maturity_diagnosis)
    col_a, col_b = st.columns(2)
    render_list_card(col_a, "Oportunidades de automacao", hr_plan.automation_opportunities)
    render_list_card(col_b, "Plano de treinamento", hr_plan.training_plan)
    render_list_card(st, "Analise de riscos", hr_plan.risk_analysis)
    st.subheader("Roadmap de implementacao")
    render_phase_plan(hr_plan.implementation_roadmap)
    render_list_card(st, "Indicadores de sucesso", hr_plan.success_indicators)


def render_metrics_dashboard(profile: dict[str, object], ai_mode: str) -> None:
    st.header("Dashboard")
    st.caption("Metricas simples da sessao atual, sem banco de dados.")
    metrics = build_dashboard_metrics(st.session_state, str(profile["role"]), ai_mode)
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Perguntas respondidas", metrics.questions_answered)
    col_b.metric("Diagnosticos gerados", metrics.diagnoses_generated)
    col_c.metric("Readiness medio", f"{metrics.average_readiness_score:.1f}")
    col_d, col_e = st.columns(2)
    col_d.metric("Modo IA", metrics.ai_mode)
    col_e.metric("Perfil selecionado", metrics.selected_profile)
    render_list_card(st, "Skills mais recomendadas", metrics.most_recommended_skills)


def render_export_tab(
    profile: dict[str, object],
    diagnosis: SkillDiagnosis,
    readiness: ReadinessScore,
    impact: AutomationImpact,
    study_path: list[StudyPathItem],
    personalized_path: PersonalizedStudyPath,
    plan: dict[str, list[str]],
) -> None:
    st.header("Exportar")
    st.caption("Exports simples em Markdown, sem dependencias externas.")
    full_report = build_markdown_report(
        profile=profile,
        diagnosis=diagnosis,
        readiness=readiness,
        impact=impact,
        study_path=study_path,
        plan=plan,
    )
    diagnosis_markdown = build_section_markdown(
        "Diagnostico Work4.0",
        {
            "Resumo": [diagnosis.summary, diagnosis.next_action],
            "Pontos fortes": diagnosis.strengths,
            "Lacunas": diagnosis.gaps,
            "Prioridades": diagnosis.priority_skills,
        },
    )
    study_markdown = build_section_markdown(
        "Plano de estudos Work4.0",
        {
            "Projeto de portfolio": [personalized_path.portfolio_project_suggestion],
            "Trilha semanal": [
                f"Semana {item.week}: {item.skill}. {item.objective} Entrega: {item.deliverable}."
                for item in personalized_path.weekly_path
            ],
            "Plano 30/60/90": [
                f"{phase}: {'; '.join(actions)}" for phase, actions in plan.items()
            ],
        },
    )
    col_a, col_b, col_c = st.columns(3)
    col_a.download_button(
        "Exportar relatorio completo",
        data=full_report,
        file_name="work40-ai-relatorio.md",
        mime="text/markdown",
        use_container_width=True,
    )
    col_b.download_button(
        "Exportar diagnostico",
        data=diagnosis_markdown,
        file_name="work40-ai-diagnostico.md",
        mime="text/markdown",
        use_container_width=True,
    )
    col_c.download_button(
        "Exportar plano de estudos",
        data=study_markdown,
        file_name="work40-ai-plano.md",
        mime="text/markdown",
        use_container_width=True,
    )
    st.subheader("Previa do relatorio completo")
    st.code(full_report, language="markdown")


def render_list_card(parent: Any, title: str, items: list[str]) -> None:
    with parent.container(border=True):
        st.subheader(title)
        if not items:
            st.caption("Nenhum item registrado ainda.")
            return
        for item in items:
            st.markdown(f"- {item}")


def render_phase_plan(plan: dict[str, list[str]]) -> None:
    columns = st.columns(len(plan))
    for column, (phase, actions) in zip(columns, plan.items(), strict=False):
        render_list_card(column, phase, actions)


def render_app(profile: dict[str, object], rag: RAGPipeline) -> None:
    ensure_metrics_state(st.session_state)
    settings = get_settings()
    view = build_view_model(profile, settings)
    render_hero(profile, str(view["ai_mode"]))
    render_key_metrics(
        view["readiness"],
        view["impact"],
        view["diagnosis"],
        str(view["ai_mode"]),
    )
    tabs = st.tabs(
        [
            "Visao geral",
            "Assistente RAG",
            "Diagnostico",
            "Plano de estudos",
            "Simulador de automacao",
            "Modo Professor",
            "Modo Empresa/RH",
            "Dashboard",
            "Exportar",
        ]
    )
    with tabs[0]:
        render_overview(
            profile,
            view["readiness"],
            view["diagnosis"],
            view["impact"],
            view["personalized_path"],
        )
    with tabs[1]:
        render_assistant_tab(profile, rag, settings)
    with tabs[2]:
        render_diagnosis_tab(view["diagnosis"], view["readiness"])
    with tabs[3]:
        render_study_plan_tab(view["personalized_path"], view["plan"])
    with tabs[4]:
        render_automation_tab(profile, list(profile["selected_skills"]), view["impact"])
    with tabs[5]:
        render_teacher_mode_tab(view["teacher_plan"])
    with tabs[6]:
        render_company_mode_tab(view["hr_plan"])
    with tabs[7]:
        render_metrics_dashboard(profile, str(view["ai_mode"]))
    with tabs[8]:
        render_export_tab(
            profile,
            view["diagnosis"],
            view["readiness"],
            view["impact"],
            view["study_path"],
            view["personalized_path"],
            view["plan"],
        )


def main() -> None:
    render_page_styles()
    profile = render_sidebar()
    rag = get_rag_pipeline()
    render_app(profile, rag)


if __name__ == "__main__":
    main()

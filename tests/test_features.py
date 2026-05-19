from src.features.automation import simulate_automation_impact
from src.features.dashboard import (
    build_dashboard_metrics,
    initial_metrics_state,
    record_diagnosis,
    record_question_answered,
)
from src.features.modes import generate_company_hr_plan, generate_teacher_mode_plan
from src.features.planning import (
    build_personalized_study_path,
    generate_30_60_90_plan,
    recommend_study_path,
)
from src.features.readiness import calculate_readiness_score
from src.features.skills import diagnose_skills
from src.ui.markdown_export import build_markdown_report, build_section_markdown


def test_diagnose_skills_finds_gaps_and_priorities() -> None:
    diagnosis = diagnose_skills(["Dados"], "Analista de dados industriais")

    assert "Python" in diagnosis.gaps
    assert diagnosis.coverage_ratio > 0
    assert diagnosis.priority_skills
    assert diagnosis.next_action
    assert diagnosis.category_scores["Dados"] == 100


def test_readiness_score_has_component_scores_and_is_bounded() -> None:
    readiness = calculate_readiness_score(
        technical_skills=1.0,
        learning_hours_per_week=50,
        adaptability=1.0,
        collaboration=1.0,
    )

    assert readiness.score == 100
    assert readiness.digital_readiness_score == 100
    assert readiness.ai_readiness_score == 100
    assert readiness.automation_readiness_score == 100
    assert readiness.career_adaptability_score == 100
    assert readiness.general_work40_score == 100
    assert readiness.scoring_notes


def test_automation_impact_decreases_with_digital_skills_and_maturity() -> None:
    baseline = simulate_automation_impact(
        "Operacoes",
        [],
        main_tasks=["preencher relatorio", "conferir dados"],
        digital_maturity="Inicial",
    )
    prepared = simulate_automation_impact(
        "Operacoes",
        ["Dados", "Automacao", "IA generativa", "Comunicacao"],
        main_tasks=["preencher relatorio", "conferir dados"],
        digital_maturity="Avancado",
    )

    assert prepared.score < baseline.score
    assert baseline.tasks_more_likely_automated
    assert prepared.opportunity_level in {"Alto", "Medio", "Inicial"}
    assert prepared.adaptation_plan


def test_personalized_study_path_returns_weekly_deliverables() -> None:
    path = build_personalized_study_path(
        user_profile="Estudante",
        current_level="Inicial",
        goal="Analista de dados industriais",
        available_hours_per_week=6,
        timeframe_weeks=4,
        gaps=["Python", "Dados", "GitHub/portfolio"],
    )

    assert path.weekly_path
    assert path.objectives
    assert path.practical_deliverables
    assert "portfolio" in path.portfolio_project_suggestion.lower()


def test_recommend_study_path_keeps_backward_compatible_items() -> None:
    items = recommend_study_path(["Python"], 4)

    assert items[0].skill == "Python"
    assert items[0].recommendation
    assert items[0].week == 1


def test_30_60_90_plan_supports_profile_types() -> None:
    plan = generate_30_60_90_plan("Professor", "Ensinar IA aplicada")

    assert set(plan) == {"30 dias", "60 dias", "90 dias"}
    assert "aula" in " ".join(plan["60 dias"]).lower() or plan["60 dias"]


def test_teacher_mode_generates_class_assets() -> None:
    plan = generate_teacher_mode_plan("IA e trabalho", "turma tecnica")

    assert plan.lesson_plan
    assert plan.learning_objectives
    assert plan.class_activity
    assert plan.debate_questions
    assert plan.practical_project
    assert plan.evaluation_criteria


def test_company_hr_mode_generates_roadmap_and_indicators() -> None:
    plan = generate_company_hr_plan("Operacoes", "Intermediario", ["Operacoes"])

    assert plan.digital_maturity_diagnosis
    assert plan.automation_opportunities
    assert plan.training_plan
    assert plan.risk_analysis
    assert "30 dias" in plan.implementation_roadmap
    assert plan.success_indicators


def test_dashboard_metrics_use_session_like_state() -> None:
    state = initial_metrics_state()
    record_question_answered(state)
    record_diagnosis(state, 70, ["Python", "Dados", "Python"])

    metrics = build_dashboard_metrics(state, "Estudante", "offline")

    assert metrics.questions_answered == 1
    assert metrics.diagnoses_generated == 1
    assert metrics.average_readiness_score == 70
    assert metrics.most_recommended_skills[0] == "Python"
    assert metrics.ai_mode == "offline"


def test_markdown_export_includes_richer_sections() -> None:
    diagnosis = diagnose_skills(["Dados"], "Analista de dados industriais")
    readiness = calculate_readiness_score(0.5, 6, 0.7, 0.8)
    impact = simulate_automation_impact("Operacoes", ["Dados"])
    study_path = recommend_study_path(diagnosis.priority_skills, 6)
    plan = generate_30_60_90_plan("Estudante", "Analista", study_path)

    report = build_markdown_report(
        profile={
            "role": "Estudante",
            "career_goal": "Analista",
            "current_role": "Operacoes",
        },
        diagnosis=diagnosis,
        readiness=readiness,
        impact=impact,
        study_path=study_path,
        plan=plan,
    )
    section = build_section_markdown("Resumo", ["Item"])

    assert "Digital Readiness Score" in report
    assert "Tarefas mais expostas" in report
    assert section.startswith("# Resumo")

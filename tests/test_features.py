from src.features.automation import simulate_automation_impact
from src.features.readiness import calculate_readiness_score
from src.features.skills import diagnose_skills


def test_diagnose_skills_finds_gaps() -> None:
    diagnosis = diagnose_skills(["Dados"], "Analista de dados industriais")

    assert "Python" in diagnosis.gaps
    assert diagnosis.coverage_ratio == 0.2


def test_readiness_score_is_bounded() -> None:
    readiness = calculate_readiness_score(
        technical_skills=1.0,
        learning_hours_per_week=50,
        adaptability=1.0,
        collaboration=1.0,
    )

    assert readiness.score == 100


def test_automation_impact_decreases_with_digital_skills() -> None:
    baseline = simulate_automation_impact("Operacoes", [])
    prepared = simulate_automation_impact(
        "Operacoes",
        ["Dados", "Automacao", "IA generativa", "Comunicacao"],
    )

    assert prepared.score < baseline.score

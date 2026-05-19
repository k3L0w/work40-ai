from __future__ import annotations

from dataclasses import dataclass


ROLE_SKILL_MAP = {
    "analista de dados industriais": [
        "Dados",
        "Python",
        "IoT",
        "Automacao",
        "Comunicacao",
    ],
    "tecnico de automacao": [
        "Automacao",
        "Robotica",
        "IoT",
        "Dados",
        "Gestao de mudanca",
    ],
    "default": [
        "Dados",
        "Automacao",
        "IA generativa",
        "Comunicacao",
        "Gestao de mudanca",
    ],
}


@dataclass(frozen=True)
class SkillDiagnosis:
    required_skills: list[str]
    gaps: list[str]
    coverage_ratio: float
    summary: str


def diagnose_skills(current_skills: list[str], career_goal: str) -> SkillDiagnosis:
    normalized_goal = career_goal.strip().lower()
    required = ROLE_SKILL_MAP.get(normalized_goal, ROLE_SKILL_MAP["default"])
    current = set(current_skills)
    gaps = [skill for skill in required if skill not in current]
    coverage = (len(required) - len(gaps)) / len(required)
    summary = (
        f"Voce cobre {coverage:.0%} das competencias prioritarias para "
        f"'{career_goal}'."
    )
    return SkillDiagnosis(
        required_skills=required,
        gaps=gaps,
        coverage_ratio=coverage,
        summary=summary,
    )

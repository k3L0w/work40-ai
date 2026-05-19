from __future__ import annotations

from dataclasses import dataclass, field


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
        "Alfabetizacao digital",
        "Python",
        "Dados",
        "IA generativa",
        "Automacao",
        "GitHub/portfolio",
        "Comunicacao",
        "Adaptabilidade",
    ],
}

SKILL_CATEGORIES = {
    "Alfabetizacao digital": ("Alfabetizacao digital", "Dados", "IoT"),
    "Python": ("Python",),
    "Dados": ("Dados",),
    "IA generativa": ("IA generativa",),
    "Automacao": ("Automacao", "Robotica"),
    "GitHub/portfolio": ("GitHub", "Portfolio", "GitHub/portfolio"),
    "Comunicacao": ("Comunicacao",),
    "Adaptabilidade": ("Adaptabilidade", "Gestao de mudanca"),
}


@dataclass(frozen=True)
class SkillDiagnosis:
    required_skills: list[str]
    gaps: list[str]
    coverage_ratio: float
    summary: str
    strengths: list[str] = field(default_factory=list)
    priority_skills: list[str] = field(default_factory=list)
    next_action: str = ""
    category_scores: dict[str, int] = field(default_factory=dict)


def diagnose_skills(current_skills: list[str], career_goal: str) -> SkillDiagnosis:
    normalized_goal = career_goal.strip().lower()
    goal_required = ROLE_SKILL_MAP.get(normalized_goal, ROLE_SKILL_MAP["default"])
    required = _dedupe([*ROLE_SKILL_MAP["default"], *goal_required])
    current = set(current_skills)
    category_scores = _score_categories(current)
    strengths = [name for name, score in category_scores.items() if score == 100]
    gaps = [skill for skill in required if not _has_skill(skill, current)]
    priority_skills = _prioritize_gaps(gaps, category_scores)
    coverage = (len(required) - len(gaps)) / len(required)
    next_action = _next_action(priority_skills, career_goal)
    summary = (
        f"Voce cobre {coverage:.0%} das competencias prioritarias para "
        f"'{career_goal}'. Pontos fortes: {_join_or_default(strengths)}. "
        f"Prioridade imediata: {_join_or_default(priority_skills[:3])}."
    )
    return SkillDiagnosis(
        required_skills=required,
        gaps=gaps,
        coverage_ratio=coverage,
        summary=summary,
        strengths=strengths,
        priority_skills=priority_skills,
        next_action=next_action,
        category_scores=category_scores,
    )


def _score_categories(current_skills: set[str]) -> dict[str, int]:
    return {
        category: 100 if any(skill in current_skills for skill in aliases) else 0
        for category, aliases in SKILL_CATEGORIES.items()
    }


def _has_skill(skill: str, current_skills: set[str]) -> bool:
    aliases = SKILL_CATEGORIES.get(skill, (skill,))
    return any(alias in current_skills for alias in aliases)


def _prioritize_gaps(gaps: list[str], category_scores: dict[str, int]) -> list[str]:
    priority_order = [
        "Alfabetizacao digital",
        "Dados",
        "IA generativa",
        "Automacao",
        "Python",
        "GitHub/portfolio",
        "Comunicacao",
        "Adaptabilidade",
    ]
    ranked = [skill for skill in priority_order if skill in gaps]
    ranked.extend(skill for skill in gaps if skill not in ranked)
    return [skill for skill in ranked if category_scores.get(skill, 0) < 100]


def _next_action(priority_skills: list[str], career_goal: str) -> str:
    if not priority_skills:
        return (
            "Organize evidencias em portfolio e escolha um projeto aplicado para "
            f"aproximar seu perfil do objetivo '{career_goal}'."
        )
    first = priority_skills[0]
    return (
        f"Comece por {first}: estude um fundamento, aplique em uma tarefa pequena "
        "e registre o resultado em portfolio."
    )


def _join_or_default(items: list[str], default: str = "nenhum ainda") -> str:
    return ", ".join(items) if items else default


def _dedupe(items: list[str]) -> list[str]:
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

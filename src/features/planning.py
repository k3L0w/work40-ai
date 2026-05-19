from __future__ import annotations

from dataclasses import dataclass


PROFILE_PLAN_FOCUS = {
    "estudante": "construir fundamentos e portfolio inicial",
    "trabalhador": "reposicionar experiencias e reduzir lacunas digitais",
    "trabalhador em transicao": "reposicionar experiencias e reduzir lacunas digitais",
    "professor": "transformar conteudo em experiencias praticas de aprendizagem",
    "empresa / rh": "organizar reskilling, mobilidade interna e indicadores",
    "empresa": "organizar reskilling, mobilidade interna e indicadores",
}


@dataclass(frozen=True)
class StudyPathItem:
    skill: str
    recommendation: str
    week: int = 1
    objective: str = ""
    deliverable: str = ""


@dataclass(frozen=True)
class PersonalizedStudyPath:
    weekly_path: list[StudyPathItem]
    objectives: list[str]
    practical_deliverables: list[str]
    portfolio_project_suggestion: str


def recommend_study_path(
    gaps: list[str],
    weekly_hours: int,
    user_profile: str = "Estudante",
    current_level: str = "Inicial",
    goal: str = "",
    timeframe_weeks: int = 4,
) -> list[StudyPathItem]:
    if not gaps:
        gaps = ["IA generativa", "Automacao", "Dados"]
    pace = "intensivo" if weekly_hours >= 8 else "essencial"
    weeks = max(1, timeframe_weeks)
    selected_gaps = gaps[: min(weeks, 6)]
    return [
        StudyPathItem(
            week=index + 1,
            skill=gap,
            objective=_objective_for(gap, current_level, goal),
            deliverable=_deliverable_for(gap),
            recommendation=(
                f"Estudar no ritmo {pace}, com pratica semanal e um mini projeto "
                f"aplicado ao perfil {user_profile}."
            ),
        )
        for index, gap in enumerate(selected_gaps)
    ]


def build_personalized_study_path(
    user_profile: str,
    current_level: str,
    goal: str,
    available_hours_per_week: int,
    timeframe_weeks: int,
    gaps: list[str],
) -> PersonalizedStudyPath:
    weekly_path = recommend_study_path(
        gaps=gaps,
        weekly_hours=available_hours_per_week,
        user_profile=user_profile,
        current_level=current_level,
        goal=goal,
        timeframe_weeks=timeframe_weeks,
    )
    objectives = [item.objective for item in weekly_path]
    deliverables = [item.deliverable for item in weekly_path]
    project_skill = weekly_path[0].skill if weekly_path else "Dados"
    return PersonalizedStudyPath(
        weekly_path=weekly_path,
        objectives=objectives,
        practical_deliverables=deliverables,
        portfolio_project_suggestion=(
            f"Criar um projeto de portfolio usando {project_skill} para resolver "
            f"um problema ligado ao objetivo '{goal}'."
        ),
    )


def build_plan(
    study_path: list[StudyPathItem],
    career_goal: str,
    profile_type: str = "Estudante",
) -> dict[str, list[str]]:
    return generate_30_60_90_plan(profile_type, career_goal, study_path)


def generate_30_60_90_plan(
    profile_type: str,
    goal: str,
    study_path: list[StudyPathItem] | None = None,
) -> dict[str, list[str]]:
    study_path = study_path or []
    skills = [item.skill for item in study_path] or ["Dados", "Automacao"]
    first_skill = skills[0]
    second_skill = skills[min(1, len(skills) - 1)]
    focus = PROFILE_PLAN_FOCUS.get(profile_type.strip().lower(), PROFILE_PLAN_FOCUS["estudante"])
    return {
        "30 dias": [
            f"Definir meta clara para {goal} e foco em {focus}.",
            f"Completar fundamentos de {first_skill}.",
            "Documentar aprendizados e evidencias em um diario de progresso.",
        ],
        "60 dias": [
            f"Criar um projeto simples combinando {first_skill} e {second_skill}.",
            "Coletar feedback de professor, mentor, lider ou pares.",
            "Atualizar curriculo, material didatico ou plano interno com evidencias.",
        ],
        "90 dias": [
            "Publicar ou apresentar portfolio com resultados observaveis.",
            "Simular entrevista, aula, reuniao executiva ou demonstracao do projeto.",
            "Escolher a proxima trilha de especializacao com base no feedback.",
        ],
    }


def _objective_for(skill: str, current_level: str, goal: str) -> str:
    return (
        f"Sair do nivel {current_level} em {skill} com uma aplicacao pequena "
        f"relacionada a '{goal}'."
    )


def _deliverable_for(skill: str) -> str:
    deliverables = {
        "Python": "script simples documentado no GitHub",
        "Dados": "mini dashboard ou analise exploratoria",
        "IA generativa": "promptbook com casos de uso e limites",
        "Automacao": "fluxo automatizado ou checklist de processo",
        "GitHub/portfolio": "repositorio com README e evidencias",
        "Comunicacao": "apresentacao curta do projeto",
        "Adaptabilidade": "retrospectiva de aprendizagem e proximos passos",
    }
    return deliverables.get(skill, f"evidencia pratica de {skill}")

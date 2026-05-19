from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StudyPathItem:
    skill: str
    recommendation: str


def recommend_study_path(gaps: list[str], weekly_hours: int) -> list[StudyPathItem]:
    if not gaps:
        gaps = ["IA generativa", "Automacao", "Dados"]
    pace = "intensivo" if weekly_hours >= 8 else "essencial"
    return [
        StudyPathItem(
            skill=gap,
            recommendation=(
                f"Estudar no ritmo {pace}, com pratica semanal e um mini projeto "
                "aplicado ao contexto profissional."
            ),
        )
        for gap in gaps[:5]
    ]


def build_plan(
    study_path: list[StudyPathItem],
    career_goal: str,
) -> dict[str, list[str]]:
    skills = [item.skill for item in study_path] or ["Dados", "Automacao"]
    first_skill = skills[0]
    second_skill = skills[min(1, len(skills) - 1)]
    return {
        "30 dias": [
            f"Definir meta clara para {career_goal}.",
            f"Completar fundamentos de {first_skill}.",
            "Documentar aprendizados em um diario de progresso.",
        ],
        "60 dias": [
            f"Criar um projeto simples combinando {first_skill} e {second_skill}.",
            "Coletar feedback de professor, mentor ou lider.",
            "Atualizar curriculo e perfil profissional com evidencias.",
        ],
        "90 dias": [
            "Publicar portfolio com resultados mensuraveis.",
            "Simular entrevista ou apresentacao executiva do projeto.",
            "Escolher a proxima trilha de especializacao.",
        ],
    }

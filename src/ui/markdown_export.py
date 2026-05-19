from __future__ import annotations

from src.features.automation import AutomationImpact
from src.features.planning import StudyPathItem
from src.features.readiness import ReadinessScore
from src.features.skills import SkillDiagnosis


def build_markdown_report(
    profile: dict[str, object],
    diagnosis: SkillDiagnosis,
    readiness: ReadinessScore,
    impact: AutomationImpact,
    study_path: list[StudyPathItem],
    plan: dict[str, list[str]],
) -> str:
    lines = [
        "# Work4.0 AI Career Report",
        "",
        f"- Modo: {profile['role']}",
        f"- Objetivo: {profile['career_goal']}",
        f"- Area atual: {profile['current_role']}",
        f"- Readiness Score: {readiness.score}/100",
        f"- Impacto de automacao: {impact.level}",
        "",
        "## Diagnostico",
        diagnosis.summary,
        "",
        "### Pontos fortes",
        *_bullets(diagnosis.strengths),
        "",
        "### Lacunas",
        *_bullets(diagnosis.gaps),
        "",
        "### Prioridades",
        *_bullets(diagnosis.priority_skills),
        "",
        "### Proxima acao",
        diagnosis.next_action,
        "",
        "## Readiness",
        f"- Digital Readiness Score: {readiness.digital_readiness_score}/100",
        f"- AI Readiness Score: {readiness.ai_readiness_score}/100",
        f"- Automation Readiness Score: {readiness.automation_readiness_score}/100",
        f"- Career Adaptability Score: {readiness.career_adaptability_score}/100",
        f"- General Work4.0 Score: {readiness.general_work40_score}/100",
        "",
        "## Trilha de estudo",
    ]
    lines.extend(
        f"- Semana {item.week}: {item.skill} — {item.objective}. Entrega: {item.deliverable}."
        for item in study_path
    )
    lines.extend(["", "## Plano 30/60/90"])
    for phase, actions in plan.items():
        lines.append(f"### {phase}")
        lines.extend(f"- {action}" for action in actions)
    lines.extend(
        [
            "",
            "## Simulador de automacao",
            impact.summary,
            "",
            "### Tarefas mais expostas",
            *_bullets(impact.tasks_more_likely_automated),
            "",
            "### Tarefas com julgamento humano",
            *_bullets(impact.human_judgment_tasks),
            "",
            "### Plano de adaptacao",
            *_bullets(impact.adaptation_plan),
        ]
    )
    return "\n".join(lines).strip() + "\n"


def build_section_markdown(title: str, items: list[str] | dict[str, list[str]]) -> str:
    lines = [f"# {title}", ""]
    if isinstance(items, dict):
        for section, section_items in items.items():
            lines.append(f"## {section}")
            lines.extend(_bullets(section_items))
            lines.append("")
    else:
        lines.extend(_bullets(items))
    return "\n".join(lines).strip() + "\n"


def _bullets(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items] if items else ["- Nao informado"]

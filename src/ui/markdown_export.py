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
        "## Lacunas",
    ]
    lines.extend(f"- {gap}" for gap in diagnosis.gaps)
    lines.extend(["", "## Trilha de estudo"])
    lines.extend(f"- {item.skill}: {item.recommendation}" for item in study_path)
    lines.extend(["", "## Plano 30/60/90"])
    for phase, actions in plan.items():
        lines.append(f"### {phase}")
        lines.extend(f"- {action}" for action in actions)
    lines.extend(["", "## Simulador de automacao", impact.summary])
    return "\n".join(lines).strip() + "\n"

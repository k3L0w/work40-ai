from __future__ import annotations

from dataclasses import dataclass, field


TASK_AUTOMATION_KEYWORDS = (
    "digitar",
    "copiar",
    "lançar",
    "lancar",
    "conferir",
    "relatorio",
    "relatório",
    "cadastro",
    "repetitiva",
    "planilha",
)
TASK_HUMAN_KEYWORDS = (
    "negociar",
    "decidir",
    "liderar",
    "ensinar",
    "atender",
    "criar",
    "planejar",
    "resolver",
    "avaliar",
)
DIGITAL_MATURITY_FACTORS = {
    "inicial": 0,
    "basico": 8,
    "básico": 8,
    "intermediario": 16,
    "intermediário": 16,
    "avancado": 24,
    "avançado": 24,
}


@dataclass(frozen=True)
class AutomationImpact:
    score: int
    level: str
    summary: str
    recommended_actions: list[str]
    tasks_more_likely_automated: list[str] = field(default_factory=list)
    human_judgment_tasks: list[str] = field(default_factory=list)
    risk_level: str = "Medio"
    opportunity_level: str = "Medio"
    recommended_skills: list[str] = field(default_factory=list)
    adaptation_plan: list[str] = field(default_factory=list)


def simulate_automation_impact(
    role: str,
    skills: list[str] | None = None,
    main_tasks: list[str] | None = None,
    digital_maturity: str = "Inicial",
) -> AutomationImpact:
    skills = skills or []
    tasks = main_tasks or _default_tasks_for_role(role)
    base_risk = _base_risk(role, tasks)
    mitigation = _skill_mitigation(skills) + _maturity_mitigation(digital_maturity)
    score = max(10, min(90, base_risk - mitigation))
    risk_level = _risk_level(score)
    opportunity_level = _opportunity_level(score, mitigation)
    automated_tasks = _automatable_tasks(tasks)
    human_tasks = _human_judgment_tasks(tasks)
    recommended_skills = _recommended_skills(skills, automated_tasks)
    adaptation_plan = _adaptation_plan(recommended_skills, automated_tasks)
    return AutomationImpact(
        score=score,
        level=risk_level,
        risk_level=risk_level,
        opportunity_level=opportunity_level,
        summary=(
            f"A funcao '{role}' tem exposicao estimada {risk_level.lower()} a "
            "automacao em algumas tarefas. Isso indica pontos de redesenho do "
            "trabalho, nao uma previsao deterministica sobre a profissao."
        ),
        recommended_actions=adaptation_plan,
        tasks_more_likely_automated=automated_tasks,
        human_judgment_tasks=human_tasks,
        recommended_skills=recommended_skills,
        adaptation_plan=adaptation_plan,
    )


def _base_risk(role: str, tasks: list[str]) -> int:
    role_text = role.lower()
    repetitive_roles = ["operacao", "operacoes", "administrativo", "producao"]
    role_risk = 62 if any(keyword in role_text for keyword in repetitive_roles) else 42
    task_bonus = min(18, len(_automatable_tasks(tasks)) * 6)
    return role_risk + task_bonus


def _skill_mitigation(skills: list[str]) -> int:
    mitigation = 0
    mitigation += 12 if "Dados" in skills else 0
    mitigation += 10 if "Automacao" in skills else 0
    mitigation += 8 if "IA generativa" in skills else 0
    mitigation += 6 if "Comunicacao" in skills else 0
    mitigation += 6 if "Python" in skills else 0
    return mitigation


def _maturity_mitigation(digital_maturity: str) -> int:
    return DIGITAL_MATURITY_FACTORS.get(digital_maturity.strip().lower(), 0)


def _risk_level(score: int) -> str:
    if score >= 65:
        return "Alto"
    if score >= 40:
        return "Medio"
    return "Baixo"


def _opportunity_level(score: int, mitigation: int) -> str:
    if mitigation >= 30 or score <= 35:
        return "Alto"
    if mitigation >= 14 or score <= 60:
        return "Medio"
    return "Inicial"


def _automatable_tasks(tasks: list[str]) -> list[str]:
    selected = [task for task in tasks if _contains_any(task, TASK_AUTOMATION_KEYWORDS)]
    return selected or ["Mapear tarefas repetitivas e baseadas em regras"]


def _human_judgment_tasks(tasks: list[str]) -> list[str]:
    selected = [task for task in tasks if _contains_any(task, TASK_HUMAN_KEYWORDS)]
    return selected or ["Tomada de decisao contextual e comunicacao com pessoas"]


def _recommended_skills(skills: list[str], automated_tasks: list[str]) -> list[str]:
    baseline = ["Dados", "Automacao", "IA generativa", "Comunicacao", "Portfolio"]
    if automated_tasks:
        baseline.insert(1, "Mapeamento de processos")
    return [skill for skill in baseline if skill not in skills][:5]


def _adaptation_plan(
    recommended_skills: list[str], automated_tasks: list[str]
) -> list[str]:
    first_skill = recommended_skills[0] if recommended_skills else "Portfolio"
    first_task = automated_tasks[0] if automated_tasks else "uma rotina repetitiva"
    return [
        f"Mapear '{first_task}' e separar etapas repetitivas de etapas de julgamento.",
        f"Estudar {first_skill} com um exercicio aplicado ao contexto real.",
        "Criar uma evidencia simples de melhoria, como checklist, planilha automatizada ou dashboard.",
    ]


def _default_tasks_for_role(role: str) -> list[str]:
    role_text = role.lower()
    if "professor" in role_text:
        return ["planejar aulas", "avaliar aprendizagem", "orientar estudantes"]
    if "rh" in role_text or "empresa" in role_text:
        return ["analisar planilhas", "planejar treinamentos", "conduzir conversas"]
    return ["preencher relatorio", "conferir dados", "resolver problemas operacionais"]


def _contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in keywords)

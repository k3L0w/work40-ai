from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AutomationImpact:
    score: int
    level: str
    summary: str
    recommended_actions: list[str]


def simulate_automation_impact(role: str, skills: list[str]) -> AutomationImpact:
    role_text = role.lower()
    repetitive_keywords = ["operacao", "operacoes", "administrativo", "producao"]
    risk = 62 if any(keyword in role_text for keyword in repetitive_keywords) else 42
    mitigation = 0
    mitigation += 12 if "Dados" in skills else 0
    mitigation += 10 if "Automacao" in skills else 0
    mitigation += 8 if "IA generativa" in skills else 0
    mitigation += 6 if "Comunicacao" in skills else 0
    score = max(10, min(90, risk - mitigation))

    if score >= 65:
        level = "Alto"
    elif score >= 40:
        level = "Medio"
    else:
        level = "Baixo"

    return AutomationImpact(
        score=score,
        level=level,
        summary=(
            f"A funcao '{role}' tem impacto estimado {level.lower()} porque tarefas "
            "repetitivas podem ser automatizadas, enquanto competencias digitais e "
            "humanas reduzem o risco."
        ),
        recommended_actions=[
            "Mapear tarefas repetitivas e identificar onde IA pode apoiar decisoes.",
            "Aprender fundamentos de dados e automacao de processos.",
            "Criar um portfolio com um caso pratico de melhoria operacional.",
        ],
    )

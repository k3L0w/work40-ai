from __future__ import annotations

from dataclasses import dataclass, field


# Simple MVP scoring rules:
# - Digital readiness: current technical coverage plus study rhythm.
# - AI readiness: technical coverage adjusted by continuous learning.
# - Automation readiness: technical coverage plus collaboration for redesign work.
# - Career adaptability: adaptability, collaboration and available learning time.
# - General score: weighted average of the four component scores.


@dataclass(frozen=True)
class ReadinessScore:
    score: int
    summary: str
    digital_readiness_score: int = 0
    ai_readiness_score: int = 0
    automation_readiness_score: int = 0
    career_adaptability_score: int = 0
    general_work40_score: int = 0
    scoring_notes: list[str] = field(default_factory=list)


def calculate_readiness_score(
    technical_skills: float,
    learning_hours_per_week: int,
    adaptability: float,
    collaboration: float,
) -> ReadinessScore:
    technical = _clamp_ratio(technical_skills)
    learning = min(1.0, max(0, learning_hours_per_week) / 10)
    adaptability = _clamp_ratio(adaptability)
    collaboration = _clamp_ratio(collaboration)

    digital = _to_score(technical * 0.7 + learning * 0.3)
    ai = _to_score(technical * 0.6 + learning * 0.25 + adaptability * 0.15)
    automation = _to_score(technical * 0.55 + collaboration * 0.25 + learning * 0.2)
    career = _to_score(adaptability * 0.5 + collaboration * 0.3 + learning * 0.2)
    general = round(digital * 0.3 + ai * 0.25 + automation * 0.25 + career * 0.2)
    summary = _summary_for_score(general)
    return ReadinessScore(
        score=general,
        summary=summary,
        digital_readiness_score=digital,
        ai_readiness_score=ai,
        automation_readiness_score=automation,
        career_adaptability_score=career,
        general_work40_score=general,
        scoring_notes=[
            "Pontuacao baseada em cobertura tecnica, horas de estudo, adaptabilidade e colaboracao.",
            "O resultado e uma estimativa orientativa, nao uma previsao de carreira.",
        ],
    )


def _summary_for_score(score: int) -> str:
    if score >= 75:
        return "Alta prontidao para desafios da Industria 4.0."
    if score >= 50:
        return "Prontidao intermediaria; priorize gaps tecnicos e portfolio."
    return "Prontidao inicial; comece com fundamentos digitais e rotina de estudo."


def _to_score(value: float) -> int:
    return round(_clamp_ratio(value) * 100)


def _clamp_ratio(value: float) -> float:
    return max(0.0, min(1.0, value))

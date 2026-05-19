from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReadinessScore:
    score: int
    summary: str


def calculate_readiness_score(
    technical_skills: float,
    learning_hours_per_week: int,
    adaptability: float,
    collaboration: float,
) -> ReadinessScore:
    learning_factor = min(1.0, learning_hours_per_week / 10)
    raw_score = (
        technical_skills * 0.4
        + learning_factor * 0.25
        + adaptability * 0.2
        + collaboration * 0.15
    )
    score = round(raw_score * 100)
    if score >= 75:
        summary = "Alta prontidao para desafios da Industria 4.0."
    elif score >= 50:
        summary = "Prontidao intermediaria; priorize gaps tecnicos e portfolio."
    else:
        summary = "Prontidao inicial; comece com fundamentos digitais e rotina de estudo."
    return ReadinessScore(score=score, summary=summary)

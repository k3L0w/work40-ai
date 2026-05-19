from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import MutableMapping


@dataclass(frozen=True)
class DashboardMetrics:
    questions_answered: int = 0
    diagnoses_generated: int = 0
    average_readiness_score: float = 0.0
    most_recommended_skills: list[str] = field(default_factory=list)
    selected_profile: str = "Estudante"
    ai_mode: str = "offline"


def initial_metrics_state() -> dict[str, object]:
    return {
        "questions_answered": 0,
        "diagnoses_generated": 0,
        "readiness_scores": [],
        "recommended_skills": [],
    }


def ensure_metrics_state(state: MutableMapping[str, object]) -> None:
    for key, value in initial_metrics_state().items():
        state.setdefault(key, value)


def record_question_answered(state: MutableMapping[str, object]) -> None:
    ensure_metrics_state(state)
    state["questions_answered"] = int(state["questions_answered"]) + 1


def record_diagnosis(
    state: MutableMapping[str, object],
    readiness_score: int,
    recommended_skills: list[str],
) -> None:
    ensure_metrics_state(state)
    state["diagnoses_generated"] = int(state["diagnoses_generated"]) + 1
    scores = list(state["readiness_scores"])
    scores.append(readiness_score)
    state["readiness_scores"] = scores
    skills = list(state["recommended_skills"])
    skills.extend(recommended_skills)
    state["recommended_skills"] = skills


def build_dashboard_metrics(
    state: MutableMapping[str, object],
    selected_profile: str,
    ai_mode: str,
) -> DashboardMetrics:
    ensure_metrics_state(state)
    scores = [int(score) for score in state["readiness_scores"]]
    skills = [str(skill) for skill in state["recommended_skills"]]
    average = round(sum(scores) / len(scores), 1) if scores else 0.0
    most_common = [skill for skill, _count in Counter(skills).most_common(5)]
    return DashboardMetrics(
        questions_answered=int(state["questions_answered"]),
        diagnoses_generated=int(state["diagnoses_generated"]),
        average_readiness_score=average,
        most_recommended_skills=most_common,
        selected_profile=selected_profile,
        ai_mode=ai_mode,
    )

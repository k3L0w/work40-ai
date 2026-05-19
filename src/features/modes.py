from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TeacherModePlan:
    lesson_plan: list[str]
    learning_objectives: list[str]
    class_activity: str
    debate_questions: list[str]
    practical_project: str
    evaluation_criteria: list[str]


@dataclass(frozen=True)
class CompanyHRPlan:
    digital_maturity_diagnosis: str
    automation_opportunities: list[str]
    training_plan: list[str]
    risk_analysis: list[str]
    implementation_roadmap: dict[str, list[str]]
    success_indicators: list[str]


def generate_teacher_mode_plan(topic: str, audience: str = "turma") -> TeacherModePlan:
    return TeacherModePlan(
        lesson_plan=[
            f"Contextualizar {topic} no futuro do trabalho.",
            "Apresentar um caso realista de tarefa impactada por IA ou automacao.",
            "Conduzir pratica em grupos com reflexao etica e profissional.",
        ],
        learning_objectives=[
            "Identificar tarefas mais expostas a automacao.",
            "Relacionar competencias digitais e humanas a trajetorias profissionais.",
            "Produzir uma evidencia pratica de aprendizagem.",
        ],
        class_activity=(
            f"Dividir a {audience} em grupos para mapear uma profissao, listar "
            "tarefas e propor uma adaptacao com IA, dados ou automacao."
        ),
        debate_questions=[
            "Quais tarefas devem continuar sob decisao humana?",
            "Como evitar promessas exageradas sobre IA e emprego?",
            "Que evidencias demonstram aprendizagem pratica?",
        ],
        practical_project=(
            "Criar um mini portfolio com diagnostico de tarefas, competencias "
            "necessarias e proposta de melhoria responsavel."
        ),
        evaluation_criteria=[
            "Clareza do diagnostico de tarefas.",
            "Uso responsavel de conceitos de IA e automacao.",
            "Qualidade da evidencia pratica apresentada.",
        ],
    )


def generate_company_hr_plan(
    area: str,
    digital_maturity: str,
    priority_roles: list[str] | None = None,
) -> CompanyHRPlan:
    roles = priority_roles or ["Operacoes", "Administrativo", "Atendimento"]
    return CompanyHRPlan(
        digital_maturity_diagnosis=(
            f"A area {area} declara maturidade digital {digital_maturity}. O MVP "
            "recomenda validar processos, dados disponiveis e capacidade de treinamento."
        ),
        automation_opportunities=[
            f"Mapear tarefas repetitivas em {role}." for role in roles[:3]
        ],
        training_plan=[
            "Fundamentos de dados e IA generativa para todos os perfis.",
            "Automacao de processos para funcoes com rotinas repetitivas.",
            "Comunicacao, mudanca e etica para liderancas e multiplicadores.",
        ],
        risk_analysis=[
            "Evitar comunicar automacao como substituicao inevitavel de pessoas.",
            "Revisar qualidade dos dados antes de automatizar decisoes.",
            "Garantir acompanhamento humano em decisoes sensiveis.",
        ],
        implementation_roadmap={
            "30 dias": ["Diagnosticar processos", "Selecionar pilotos", "Definir indicadores"],
            "60 dias": ["Treinar multiplicadores", "Executar piloto", "Coletar feedback"],
            "90 dias": ["Medir resultados", "Ajustar governanca", "Escalar com cautela"],
        },
        success_indicators=[
            "participacao em treinamentos",
            "projetos piloto concluidos",
            "horas economizadas em tarefas repetitivas",
            "satisfacao das equipes envolvidas",
        ],
    )

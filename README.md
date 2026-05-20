# Work4.0 AI

**Work4.0 AI** e um MVP em Streamlit para inteligencia de carreira na era da
Industria 4.0. O projeto combina RAG, diagnostico de competencias, simulador de
automacao, planos de estudo e modos para professores e empresas, mantendo uma
base simples, testavel e pronta para demonstracao.

O app foi pensado para apresentacoes no SENAI, portfolio no GitHub, publicacao no
LinkedIn e avaliacao por recrutadores. Ele funciona offline por padrao e usa a
OpenAI apenas quando `OPENAI_API_KEY` esta configurada de forma segura.

## Links de producao

- Streamlit app: <https://work40-ai.streamlit.app>
- GitHub Pages landing page: <https://k3l0w.github.io/work40-ai/>
- GitHub repository: <https://github.com/k3L0w/work40-ai>

## Product Pitch

Profissionais, estudantes, professores e equipes de RH precisam transformar a
mudanca causada por IA, automacao, robotica e dados em planos praticos de
aprendizagem. Work4.0 AI entrega uma experiencia guiada para diagnosticar
competencias, entender riscos e oportunidades por tarefa, consultar uma base RAG
e gerar proximas acoes com linguagem clara.

## Problema

A transformacao digital cria duvidas recorrentes:

- quais competencias priorizar;
- quais tarefas podem ser automatizadas ou aumentadas por IA;
- como criar evidencias praticas de aprendizagem;
- como professores podem levar Industria 4.0 para a sala de aula;
- como empresas podem planejar reskilling sem discurso alarmista.

O projeto evita promessas de emprego, estatisticas inventadas e previsoes
absolutas sobre extincao de profissoes.

## Solucao

Work4.0 AI oferece:

- assistente RAG com citacao de fontes internas;
- fallback offline deterministico;
- diagnostico de competencias digitais e humanas;
- Work4.0 Readiness Score;
- simulador de impacto da automacao por tarefa;
- trilha semanal de estudos;
- plano 30/60/90 dias;
- modo Professor;
- modo Empresa/RH;
- dashboard de sessao;
- exportacao em Markdown;
- landing page estatica para GitHub Pages.

## Publico-alvo

- **Estudantes:** escolher competencias e montar portfolio.
- **Trabalhadores:** reposicionar experiencia para tarefas de maior valor.
- **Professores:** criar planos de aula, debates e projetos praticos.
- **Empresas/RH:** planejar reskilling, pilotos de automacao e indicadores.
- **Recrutadores e avaliadores:** revisar arquitetura, testes, UX e maturidade do MVP.

## Features principais

| Feature | Descricao |
| --- | --- |
| Assistente RAG | Responde em portugues usando a base local e citando arquivo/chunk. |
| Skills Diagnosis | Avalia alfabetizacao digital, Python, dados, IA, automacao, portfolio, comunicacao e adaptabilidade. |
| Readiness Score | Calcula prontidao digital, IA, automacao, adaptabilidade e score geral Work4.0. |
| Automation Simulator | Separa tarefas mais expostas, tarefas com julgamento humano, risco, oportunidade e plano. |
| Study Path | Gera trilha semanal, objetivos, entregaveis e projeto de portfolio. |
| 30/60/90 Plan | Cria plano de execucao para estudante, trabalhador, professor e empresa/RH. |
| Teacher Mode | Gera plano de aula, objetivos, atividade, debate, projeto e criterios. |
| Company/HR Mode | Gera maturidade, oportunidades, riscos, treinamento, roadmap e indicadores. |
| Dashboard | Mostra metricas da sessao sem banco de dados. |
| Markdown Export | Exporta relatorio completo, diagnostico e plano de estudos. |

## Arquitetura

```text
app/main.py                 Streamlit UI
src/ai/assistant.py         Geracao OpenAI opcional + fallback offline
src/knowledge/              Loader e RAG TF-IDF sobre data/knowledge
src/features/               Regras de diagnostico, readiness, simulador e planos
src/ui/markdown_export.py   Exportacao Markdown
data/knowledge/             Base interna em Markdown
docs/                       Landing page GitHub Pages e docs de deploy
tests/                      Testes deterministicos com pytest
```

Principios aplicados:

- UI separada da logica de negocio;
- IA separada da recuperacao RAG;
- fallback offline obrigatorio;
- ausencia de segredos hardcoded;
- testes sem chamadas reais a OpenAI;
- deploy sem infraestrutura paga obrigatoria.

## Tech Stack

- Python 3.11
- Streamlit
- scikit-learn
- pandas
- numpy
- python-dotenv
- OpenAI SDK opcional
- pytest
- ruff
- GitHub Codespaces
- GitHub Pages
- Streamlit Community Cloud

## Rodar no GitHub Codespaces

1. Abra o repositorio no GitHub.
2. Selecione **Code > Codespaces > Create codespace**.
3. Aguarde o `postCreateCommand` instalar as dependencias.
4. Rode:

```bash
streamlit run app/main.py
```

5. Abra a aba **PORTS**.
6. Localize a porta `8501`.
7. Use **Open in Browser**.

A configuracao `.streamlit/config.toml` ja usa `0.0.0.0:8501`, adequado para
Codespaces e Streamlit.

## Rodar localmente

Requisitos: Python 3.11 recomendado.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app/main.py
```

No Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app/main.py
```

## Configurar OPENAI_API_KEY com seguranca

O app funciona sem OpenAI. Para habilitar modo online localmente:

1. Copie `.env.example` para `.env`.
2. Preencha a chave apenas no arquivo local:

```bash
APP_ENV=local
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-4.1-mini
```

3. Nunca commite `.env`.
4. Nunca cole chaves em README, docs, prints, issues ou commits.

Sem `OPENAI_API_KEY`, o assistente usa fallback offline deterministico.

## Deploy no Streamlit Community Cloud

1. Publique o repositorio no GitHub.
2. Acesse <https://share.streamlit.io/>.
3. Crie um novo app.
4. Configure:
   - repository: este repositorio;
   - branch: `main` ou branch de deploy;
   - main file path: `app/main.py`.
5. Em **Advanced settings > Secrets**, adicione apenas se quiser modo online:

```toml
OPENAI_API_KEY = "sua_chave_aqui"
OPENAI_MODEL = "gpt-4.1-mini"
APP_ENV = "production"
```

Sem secrets, o app continua funcionando em modo offline.

## GitHub Pages

A landing page esta em:

- `docs/index.html`
- `docs/assets/style.css`
- <https://k3l0w.github.io/work40-ai/>

Para publicar:

1. Abra **Settings > Pages** no GitHub.
2. Escolha **Deploy from a branch**.
3. Selecione a branch principal.
4. Escolha a pasta `/docs`.
5. Salve.

Os botoes da landing page apontam para o app em producao e para o repositorio
oficial.

## Demo Questions

Use estas perguntas no Assistente RAG:

- Como devo me preparar para a Industria 4.0?
- Quais competencias devo priorizar para trabalhar com dados industriais?
- Como a automacao pode impactar tarefas repetitivas no meu cargo?
- Que habilidades humanas continuam importantes com IA e automacao?
- Como montar um portfolio para uma carreira em automacao e dados?

Mais exemplos estao em [`docs/demo_questions.md`](docs/demo_questions.md).

## Validacao

Antes de apresentar ou publicar:

```bash
pytest
ruff check .
streamlit run app/main.py --server.address 0.0.0.0 --server.port 8501
```

Para conferir a landing page, abra `docs/index.html` diretamente no navegador.

## Roadmap

- Adicionar upload controlado de documentos para expandir a base RAG.
- Criar autenticacao simples para perfis persistentes.
- Salvar historico e metricas em banco leve quando necessario.
- Adicionar screenshots reais na landing page.
- Melhorar ranking RAG com embeddings quando houver infraestrutura adequada.
- Adicionar avaliacao automatizada de qualidade das respostas.

## Limitacoes

- As metricas do dashboard usam apenas `st.session_state` e reiniciam por sessao.
- O simulador e os scores sao heuristicas de MVP, nao previsoes de mercado.
- O fallback offline e deterministico e menos flexivel que um modelo generativo.
- A base RAG e pequena e deve ser expandida para uso real.
- Links de producao configurados para Streamlit, GitHub Pages e repositorio.

## Documentacao extra

- [`docs/deployment.md`](docs/deployment.md)
- [`docs/architecture.md`](docs/architecture.md)
- [`docs/demo_script.md`](docs/demo_script.md)
- [`docs/demo_questions.md`](docs/demo_questions.md)
- [`docs/final_checklist.md`](docs/final_checklist.md)

## Seguranca e guardrails

- Sem chaves hardcoded.
- Sem chamadas obrigatorias a API externa.
- Sem promessas de emprego.
- Sem estatisticas inventadas.
- Sem previsoes absolutas sobre extincao de profissoes.
- Respostas RAG devem citar fontes internas quando houver contexto suficiente.

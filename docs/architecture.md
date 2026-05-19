# Architecture — Work4.0 AI

Work4.0 AI foi desenhado como um MVP modular, simples de explicar e facil de
executar em Codespaces, Streamlit Community Cloud e ambiente local.

## Visao geral

```text
Usuario
  |
  v
Streamlit UI (app/main.py)
  |
  +--> src/features/        regras deterministicas de produto
  +--> src/knowledge/       carregamento da base e recuperacao RAG
  +--> src/ai/assistant.py  geracao OpenAI opcional e fallback offline
  +--> src/ui/              exportacao Markdown
```

## Camadas

### Interface

`app/main.py` concentra a experiencia Streamlit:

- sidebar de perfil;
- hero e metricas principais;
- abas de produto;
- exibicao de fontes;
- botoes de exportacao.

A UI chama funcoes de negocio, mas nao implementa as regras principais.

### Features

`src/features/` contem regras deterministicas:

- `skills.py`: diagnostico de competencias;
- `readiness.py`: scores Work4.0;
- `automation.py`: simulador de automacao;
- `planning.py`: trilhas e planos 30/60/90;
- `modes.py`: modo Professor e Empresa/RH;
- `dashboard.py`: metricas de sessao.

### Conhecimento e RAG

`src/knowledge/` carrega arquivos Markdown de `data/knowledge/`, divide em chunks
e usa TF-IDF com `scikit-learn` para recuperar trechos relevantes.

A recuperacao retorna:

- titulo;
- trecho;
- score;
- arquivo;
- indice do chunk.

### IA e fallback

`src/ai/assistant.py` decide o modo de resposta:

- se `OPENAI_API_KEY` existe, tenta gerar com OpenAI;
- se a biblioteca ou a chamada falhar, usa fallback offline;
- se o contexto recuperado for insuficiente, retorna mensagem de baixa confianca;
- respostas em RAG devem citar fontes internas.

### Exportacao

`src/ui/markdown_export.py` gera relatorios Markdown sem dependencia externa.

## Dados

`data/knowledge/` contem a base interna inicial:

- Industria 4.0 e trabalho;
- automacao e redesenho de carreiras;
- competencias para a era da IA.

A base e pequena por design de MVP e pode ser expandida com novos arquivos
Markdown.

## Deploy

- Streamlit app: `app/main.py` no Streamlit Community Cloud.
- Landing page: `/docs` no GitHub Pages.
- Codespaces: porta `8501` ja configurada no devcontainer.

## Decisoes de arquitetura

- Sem banco de dados nesta fase.
- Sem dependencias pesadas de frontend.
- Sem API externa obrigatoria.
- Testes deterministicos.
- Segredos via `.env` local ou secrets do Streamlit Cloud.

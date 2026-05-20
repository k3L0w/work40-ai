# Deployment Guide — Work4.0 AI

Este guia resume como publicar o MVP em Streamlit Community Cloud e a landing
page em GitHub Pages sem expor segredos.

## 1. Checklist antes do deploy

Leia tambem `docs/final_checklist.md` antes da apresentacao final.

Rode localmente ou no Codespaces:

```bash
pytest
ruff check .
streamlit run app/main.py --server.address 0.0.0.0 --server.port 8501
```

Confirme tambem:

- `docs/index.html` abre como pagina estatica.
- `docs/assets/style.css` carrega corretamente.
- `.env` nao foi commitado.
- Links de producao foram configurados em `docs/index.html` para Streamlit e GitHub.
- Perguntas de demo em `docs/demo_questions.md` foram testadas.
- Script em `docs/demo_script.md` foi ensaiado.

## 2. Streamlit Community Cloud

1. Publique o repositorio no GitHub.
2. Acesse <https://share.streamlit.io/>.
3. Clique em **New app**.
4. Selecione o repositorio e a branch.
5. Configure o arquivo principal como:

```text
app/main.py
```

6. Deploy.

### Secrets opcionais

O app funciona sem OpenAI, mas para modo online configure secrets no painel do
Streamlit:

```toml
OPENAI_API_KEY = "sua_chave_aqui"
OPENAI_MODEL = "gpt-4.1-mini"
APP_ENV = "production"
```

Nunca coloque a chave em `README.md`, `docs/`, codigo-fonte ou prints publicos.

## 3. GitHub Pages

A landing page fica em `/docs`, pronta para GitHub Pages.

1. Abra o repositorio no GitHub.
2. Va em **Settings > Pages**.
3. Em **Source**, escolha **Deploy from a branch**.
4. Selecione a branch principal.
5. Em folder, escolha `/docs`.
6. Salve.

Os links de producao ja estao configurados em `docs/index.html`:

```text
Streamlit app: https://work40-ai.streamlit.app
GitHub Pages: https://k3l0w.github.io/work40-ai/
GitHub repository: https://github.com/k3L0w/work40-ai
```

## 4. Codespaces

No Codespaces:

```bash
streamlit run app/main.py
```

Abra a aba **PORTS**, encontre `8501` e use **Open in Browser**.

## 5. Deploy sem chave OpenAI

Sem `OPENAI_API_KEY`, o app continua disponivel com:

- RAG local
- fallback offline deterministico
- diagnostico de competencias
- readiness score
- simulador de automacao
- planos e exports Markdown

Esse modo e recomendado para demonstracoes publicas quando voce nao quer expor
ou consumir uma chave de API.

## 6. Pos-deploy

Depois de publicar:

1. Abra a landing page em desktop e mobile.
2. Confirme o botao **Acessar aplicacao** em <https://work40-ai.streamlit.app>.
3. Confirme o botao **Ver GitHub** em <https://github.com/k3L0w/work40-ai>.
4. Teste o app publicado sem secrets para confirmar o modo offline.
5. Teste novamente com secrets, se for demonstrar modo online.

## 7. Pontos para apresentacao

Para SENAI, GitHub, LinkedIn e recrutadores, destaque:

- arquitetura modular
- testes automatizados
- lint limpo
- app funcional em Streamlit
- landing page estatica em GitHub Pages
- seguranca basica de secrets
- fallback offline para demonstracao resiliente

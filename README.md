# Work4.0 AI

Work4.0 AI e um MVP em Streamlit para inteligencia de carreira na era da
Industria 4.0. O projeto ajuda estudantes, trabalhadores, professores e equipes
de RH a entender impactos de IA, automacao, robotica, dados e transformacao
digital sobre tarefas, competencias e planos de desenvolvimento.

O MVP inclui:

- Assistente RAG com fontes internas
- fallback offline deterministico quando `OPENAI_API_KEY` nao existe
- diagnostico de competencias
- Industry 4.0 Readiness Score
- simulador de impacto da automacao
- trilha personalizada de estudos
- plano 30/60/90 dias
- modo Professor
- modo Empresa/RH
- dashboard de sessao
- exportacao Markdown
- landing page estatica para GitHub Pages em `docs/`

## Stack

- Python
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
3. Aguarde o `postCreateCommand` instalar as dependencias de `requirements.txt`.
4. Rode:

```bash
streamlit run app/main.py
```

5. Abra a aba **PORTS** no Codespaces.
6. Localize a porta `8501`.
7. Use **Open in Browser** na linha da porta encaminhada.

A configuracao `.streamlit/config.toml` ja executa o Streamlit em modo headless,
em `0.0.0.0:8501`, adequado para Codespaces.

## Rodar localmente

Requisitos: Python 3.11 recomendado.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app/main.py
```

No Windows PowerShell, ative o ambiente com:

```powershell
.venv\Scripts\Activate.ps1
```

Depois abra o endereco exibido pelo Streamlit, normalmente
`http://localhost:8501`.

## Modo offline e OpenAI

O app funciona sem chave da OpenAI. Quando `OPENAI_API_KEY` nao esta configurada,
o assistente usa fallback offline deterministico e continua respondendo com base
na logica local.

Para usar OpenAI localmente:

1. Copie `.env.example` para `.env`.
2. Preencha somente no seu ambiente local:

```bash
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-4.1-mini
APP_ENV=local
```

3. Nunca publique `.env` e nunca cole chaves em codigo, README, issues ou prints.

O arquivo `.env` deve permanecer fora do Git. Use `.env.example` apenas como
modelo sem segredo real.

## Deploy no Streamlit Community Cloud

1. Suba o repositorio para o GitHub.
2. Acesse <https://share.streamlit.io/>.
3. Crie um novo app apontando para este repositorio.
4. Configure:
   - branch: `main` ou a branch de deploy
   - main file path: `app/main.py`
5. Em **Advanced settings > Secrets**, adicione a chave somente se quiser modo
   online:

```toml
OPENAI_API_KEY = "sua_chave_aqui"
OPENAI_MODEL = "gpt-4.1-mini"
APP_ENV = "production"
```

Sem secrets, o app deve continuar funcionando em modo offline.

## GitHub Pages

A landing page estatica esta em:

- `docs/index.html`
- `docs/assets/style.css`

Para habilitar GitHub Pages:

1. No GitHub, abra **Settings > Pages**.
2. Em **Build and deployment**, selecione **Deploy from a branch**.
3. Escolha a branch principal.
4. Em folder, selecione `/docs`.
5. Salve e aguarde a URL publica.

Antes de divulgar, substitua no `docs/index.html`:

- `STREAMLIT_APP_URL` pela URL do app publicado no Streamlit Cloud
- `GITHUB_REPOSITORY_URL` pela URL do repositorio no GitHub

## Validacao

Rode antes de publicar ou apresentar:

```bash
pytest
ruff check .
streamlit run app/main.py --server.address 0.0.0.0 --server.port 8501
```

Para conferir a landing page, abra `docs/index.html` diretamente no navegador.
Ela nao exige build, JavaScript ou dependencias externas obrigatorias.

## Estrutura do projeto

```text
app/
  main.py
src/
  ai/
  features/
  knowledge/
  ui/
  utils/
data/
  knowledge/
docs/
  index.html
  assets/style.css
tests/
.devcontainer/
.github/
```

## Observacoes de seguranca

- Nao hardcode chaves ou tokens.
- Nao commite `.env`.
- Configure secrets pelo painel do Streamlit Community Cloud.
- O fallback offline permite demonstrar o MVP sem depender de API paga.
- As respostas evitam prometer emprego, inventar estatisticas ou fazer previsoes
  absolutas sobre extincao de profissoes.

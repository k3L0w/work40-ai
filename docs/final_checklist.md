# Final Release Checklist — Work4.0 AI

## Codigo

- [ ] `pytest` passa.
- [ ] `ruff check .` passa.
- [ ] `streamlit run app/main.py --server.address 0.0.0.0 --server.port 8501` inicia.
- [ ] App funciona sem `OPENAI_API_KEY`.
- [ ] Nenhum teste chama OpenAI real.
- [ ] Nao ha segredos no repositorio.

## Produto

- [ ] Assistente RAG acessivel na UI.
- [ ] Diagnostico acessivel na UI.
- [ ] Plano de estudos acessivel na UI.
- [ ] Simulador de automacao acessivel na UI.
- [ ] Modo Professor acessivel na UI.
- [ ] Modo Empresa/RH acessivel na UI.
- [ ] Dashboard acessivel na UI.
- [ ] Export Markdown acessivel na UI.

## RAG e guardrails

- [ ] Respostas RAG citam fontes internas.
- [ ] Baixa confianca retorna mensagem clara.
- [ ] Fallback offline funciona.
- [ ] OpenAI so e usada quando `OPENAI_API_KEY` existe.
- [ ] Respostas evitam estatisticas inventadas.
- [ ] Respostas nao prometem emprego.
- [ ] Respostas nao fazem previsoes absolutas sobre extincao de profissoes.
- [ ] Simulador evita linguagem deterministica ou alarmista.

## Documentacao

- [ ] README inclui pitch, problema, solucao e publico-alvo.
- [ ] README inclui arquitetura, stack e features.
- [ ] README explica Codespaces, local, Streamlit Cloud e GitHub Pages.
- [ ] README explica configuracao segura de `OPENAI_API_KEY`.
- [ ] `docs/deployment.md` revisado.
- [ ] `docs/demo_script.md` revisado.
- [ ] `docs/demo_questions.md` revisado.
- [ ] `docs/architecture.md` revisado.

## Landing page

- [ ] `docs/index.html` abre no navegador.
- [ ] `docs/assets/style.css` carrega.
- [ ] Botao **Acessar aplicacao** aponta para <https://work40-ai.streamlit.app>.
- [ ] Botao **Ver GitHub** aponta para <https://github.com/k3L0w/work40-ai>.
- [ ] Placeholders de screenshots foram substituidos ou mantidos conscientemente.

## Apresentacao

- [ ] Demo de 5 a 7 minutos ensaiada.
- [ ] Perguntas exemplo testadas.
- [ ] Modo offline testado.
- [ ] Link do Streamlit validado: <https://work40-ai.streamlit.app>.
- [ ] Link do GitHub Pages validado: <https://k3l0w.github.io/work40-ai/>.
- [ ] Link do repositorio validado: <https://github.com/k3L0w/work40-ai>.

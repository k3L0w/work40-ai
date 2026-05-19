# Work4.0 AI

Work4.0 AI is a Streamlit MVP for career intelligence in the Industry 4.0 era.
It includes a local RAG assistant, skills diagnosis, readiness scoring, automation
impact simulation, a personalized study path, a 30/60/90-day plan, and Markdown
export.

## Run Locally

```bash
python -m pip install -r requirements.txt
streamlit run app/main.py
```

The app is designed to run without `OPENAI_API_KEY`. When no key is configured,
it uses a deterministic offline fallback.

## Codespaces Troubleshooting

This repository includes `.streamlit/config.toml` for local and GitHub Codespaces
development. It sets Streamlit to run headless on `0.0.0.0:8501` and disables
usage-stat collection. It does not disable CORS or XSRF protection. If those
settings are ever changed for preview troubleshooting, treat that as a
local/Codespaces-only development exception and do not carry it silently into
production deployment.

In browser-based Codespaces, avoid manually typing `localhost:8501` in the
browser address bar. Instead:

1. Start the app with `streamlit run app/main.py`.
2. Open the Codespaces **PORTS** tab.
3. Find port `8501`.
4. Use **Open in Browser** from the forwarded port row.

The devcontainer already forwards port `8501` for the Streamlit app.

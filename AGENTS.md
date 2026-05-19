# AGENTS.md — Work4.0 AI

## Agent Role

You are acting as a Senior Harness Engineer, Product Engineer and AI Application Architect responsible for building the Work4.0 AI MVP end-to-end.

You are expected to be:
- precise
- predictable
- professional
- test-oriented
- security-conscious
- product-minded
- pragmatic
- able to improve the proposed architecture when justified

This project must look like a real startup MVP, not only a course exercise.

---

## Product Vision

Work4.0 AI is an AI-powered web platform for career intelligence in the Industry 4.0 era.

The platform helps students, workers, teachers and companies understand how automation, artificial intelligence, robotics and digital transformation affect work, skills and professional development.

The application must provide:
1. AI assistant with RAG
2. skills diagnosis
3. Industry 4.0 Readiness Score
4. automation impact simulator
5. personalized study path
6. 30/60/90-day plan
7. teacher mode
8. company/HR mode
9. dashboard
10. Markdown export
11. GitHub Pages landing page
12. Streamlit deployment readiness

---

## Technical Stack

Use:
- Python
- Streamlit
- scikit-learn
- pandas
- numpy
- python-dotenv
- OpenAI SDK when OPENAI_API_KEY exists
- offline fallback when OPENAI_API_KEY does not exist
- pytest
- ruff
- GitHub Codespaces
- GitHub Pages for the landing page
- Streamlit Community Cloud for the web application

Do not require paid infrastructure for the MVP.

---

## Architecture Rules

Use this structure:

app/
  main.py
  pages/

src/
  ai/
  knowledge/
  features/
  ui/
  utils/

data/
  knowledge/
  taxonomies/

docs/
  index.html
  assets/

tests/

.devcontainer/
  devcontainer.json

.github/
  workflows/

---

## Engineering Principles

1. Keep code modular.
2. Keep functions small and testable.
3. Separate UI from business logic.
4. Separate AI generation from retrieval logic.
5. Never hardcode secrets.
6. Never commit `.env`.
7. Never require external APIs for basic functionality.
8. The app must run offline with deterministic fallback responses.
9. The app must run with:

```bash
streamlit run app/main.py
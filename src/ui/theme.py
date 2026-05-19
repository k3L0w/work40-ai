from __future__ import annotations

import html


def app_theme_css() -> str:
    """Return the Work4.0 AI Streamlit theme as one injectable CSS block."""
    return """
<style>
/* theme tokens */
:root {
  --w40-bg: #070912;
  --w40-bg-2: #0d1020;
  --w40-panel: rgba(18, 23, 45, 0.72);
  --w40-panel-strong: rgba(23, 30, 59, 0.9);
  --w40-line: rgba(126, 231, 255, 0.2);
  --w40-line-strong: rgba(171, 115, 255, 0.42);
  --w40-text: #f5f7ff;
  --w40-muted: #aeb8d8;
  --w40-cyan: #63e6ff;
  --w40-blue: #5b8cff;
  --w40-purple: #a855f7;
  --w40-red: #ff4d6d;
  --w40-green: #45f0b5;
  --w40-shadow: 0 24px 80px rgba(0, 0, 0, 0.42);
  --w40-glow: 0 0 28px rgba(99, 230, 255, 0.22);
}

.stApp {
  color: var(--w40-text);
  background:
    radial-gradient(circle at 18% 8%, rgba(168, 85, 247, 0.2), transparent 28rem),
    radial-gradient(circle at 88% 18%, rgba(99, 230, 255, 0.14), transparent 24rem),
    radial-gradient(circle at 72% 82%, rgba(255, 77, 109, 0.1), transparent 22rem),
    linear-gradient(135deg, #060712 0%, #0b1021 48%, #10102a 100%);
}

.stApp::before {
  content: "";
  position: fixed;
  inset: 0;
  pointer-events: none;
  opacity: 0.35;
  background-image:
    linear-gradient(rgba(99, 230, 255, 0.08) 1px, transparent 1px),
    linear-gradient(90deg, rgba(99, 230, 255, 0.08) 1px, transparent 1px);
  background-size: 34px 34px;
  mask-image: linear-gradient(to bottom, black, transparent 86%);
}

.block-container {
  max-width: 1280px;
  padding-top: 2rem;
  padding-bottom: 3rem;
}

h1, h2, h3, h4, h5, h6, p, li, label, span {
  letter-spacing: 0;
}

h1, h2, h3 {
  color: var(--w40-text);
}

p, li, .stMarkdown, [data-testid="stCaptionContainer"] {
  color: var(--w40-muted);
}

/* hero */
.w40-hero {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1.08fr) minmax(280px, 0.72fr);
  gap: 34px;
  align-items: center;
  overflow: hidden;
  min-height: 390px;
  margin-bottom: 22px;
  padding: 38px;
  border: 1px solid var(--w40-line-strong);
  border-radius: 18px;
  background:
    linear-gradient(135deg, rgba(23, 30, 59, 0.86), rgba(9, 13, 29, 0.8)),
    radial-gradient(circle at 12% 12%, rgba(99, 230, 255, 0.24), transparent 18rem);
  box-shadow: var(--w40-shadow), inset 0 1px 0 rgba(255, 255, 255, 0.09);
}

.w40-hero::before {
  content: "";
  position: absolute;
  inset: 0;
  opacity: 0.28;
  background:
    linear-gradient(90deg, transparent 0 48%, rgba(99, 230, 255, 0.18) 49% 50%, transparent 51%),
    linear-gradient(transparent 0 48%, rgba(168, 85, 247, 0.16) 49% 50%, transparent 51%);
  background-size: 82px 82px;
}

.w40-hero-content,
.w40-orb-stage {
  position: relative;
  z-index: 1;
}

.w40-badge-row,
.w40-status-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 20px;
}

.w40-product-badge,
.w40-status-badge {
  display: inline-flex;
  align-items: center;
  width: fit-content;
  min-height: 30px;
  padding: 6px 10px;
  border: 1px solid rgba(99, 230, 255, 0.28);
  border-radius: 999px;
  background: rgba(99, 230, 255, 0.08);
  color: #dffaff;
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
}

.w40-status-badge {
  border-color: rgba(168, 85, 247, 0.34);
  background: rgba(168, 85, 247, 0.12);
  text-transform: none;
}

.w40-hero h1 {
  margin: 14px 0 8px;
  color: #ffffff;
  font-size: clamp(2.5rem, 6vw, 5.25rem);
  line-height: 0.96;
}

.w40-hero h2 {
  margin: 0 0 16px;
  color: #c7d2fe;
  font-size: clamp(1.2rem, 2vw, 1.65rem);
  font-weight: 700;
}

.w40-hero p {
  max-width: 720px;
  color: #bfcae8;
  font-size: 1.03rem;
}

.w40-orb-stage {
  display: grid;
  min-height: 310px;
  place-items: center;
}

.w40-orb {
  position: relative;
  width: min(310px, 72vw);
  aspect-ratio: 1;
  border: 1px solid rgba(99, 230, 255, 0.38);
  border-radius: 999px;
  background:
    radial-gradient(circle at 42% 38%, rgba(255, 255, 255, 0.86), transparent 0.18rem),
    radial-gradient(circle at 36% 28%, rgba(99, 230, 255, 0.72), transparent 4.8rem),
    radial-gradient(circle at 64% 62%, rgba(168, 85, 247, 0.65), transparent 5.6rem),
    radial-gradient(circle at 48% 58%, rgba(91, 140, 255, 0.52), transparent 6.8rem),
    rgba(12, 18, 38, 0.72);
  box-shadow:
    0 0 70px rgba(99, 230, 255, 0.28),
    0 0 110px rgba(168, 85, 247, 0.18),
    inset 0 0 55px rgba(99, 230, 255, 0.18);
  animation: w40-pulse 5.8s ease-in-out infinite;
}

.w40-orb::before,
.w40-orb::after {
  content: "";
  position: absolute;
  inset: 12%;
  border: 1px solid rgba(99, 230, 255, 0.28);
  border-radius: 999px;
  background:
    linear-gradient(90deg, transparent 48%, rgba(99, 230, 255, 0.42) 49% 51%, transparent 52%),
    linear-gradient(transparent 48%, rgba(168, 85, 247, 0.32) 49% 51%, transparent 52%);
  transform: rotateX(64deg) rotateZ(0deg);
  animation: w40-rotate 12s linear infinite;
}

.w40-orb::after {
  inset: -8%;
  border-color: rgba(255, 77, 109, 0.18);
  transform: rotateX(72deg) rotateZ(90deg);
  animation-duration: 18s;
  animation-direction: reverse;
}

@keyframes w40-pulse {
  0%, 100% { transform: translateY(0) scale(1); filter: saturate(1); }
  50% { transform: translateY(-8px) scale(1.025); filter: saturate(1.18); }
}

@keyframes w40-rotate {
  to { transform: rotateX(64deg) rotateZ(360deg); }
}

/* cards */
div[data-testid="stMetric"],
.w40-glass-card,
.w40-answer-card,
.w40-source-card,
div[data-testid="stVerticalBlockBorderWrapper"] {
  border: 1px solid var(--w40-line);
  border-radius: 16px;
  background: var(--w40-panel);
  box-shadow: 0 16px 54px rgba(0, 0, 0, 0.26), inset 0 1px 0 rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(18px);
}

div[data-testid="stMetric"] {
  min-height: 118px;
  padding: 18px 18px;
  border-color: rgba(99, 230, 255, 0.26);
}

div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
  color: var(--w40-text);
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
  color: #ecfeff;
  font-weight: 900;
}

.w40-section-note {
  max-width: 760px;
  color: var(--w40-muted);
  margin-top: -8px;
}

.w40-score-summary {
  margin: 12px 0 22px;
  color: #c8d5f7;
}

.w40-glass-card,
.w40-answer-card,
.w40-source-card {
  padding: 18px;
}

.w40-answer-card {
  max-width: 920px;
  margin-bottom: 12px;
  border-color: rgba(168, 85, 247, 0.28);
}

.w40-answer-card h3,
.w40-source-card h4 {
  margin: 0 0 8px;
  color: #e9d5ff;
}

.w40-answer-card p,
.w40-source-card p {
  color: #d8def5;
  line-height: 1.68;
}

.w40-source-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 12px;
}

.w40-source-meta {
  color: #91a3d7;
  font-size: 0.82rem;
}

/* sidebar */
[data-testid="stSidebar"] {
  background:
    radial-gradient(circle at 30% 10%, rgba(168, 85, 247, 0.22), transparent 16rem),
    linear-gradient(180deg, #080b18 0%, #0c1022 100%);
  border-right: 1px solid rgba(99, 230, 255, 0.16);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
  color: var(--w40-text);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
  color: var(--w40-muted);
}

.w40-sidebar-brand {
  padding: 14px 14px 12px;
  margin-bottom: 12px;
  border: 1px solid rgba(99, 230, 255, 0.18);
  border-radius: 16px;
  background: rgba(18, 23, 45, 0.62);
}

.w40-sidebar-brand strong {
  display: block;
  color: #ffffff;
  font-size: 1.15rem;
}

.w40-sidebar-brand span {
  color: var(--w40-muted);
  font-size: 0.86rem;
}

/* controls and navigation */
.stButton > button,
.stDownloadButton > button {
  border: 1px solid rgba(99, 230, 255, 0.32);
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(99, 230, 255, 0.2), rgba(168, 85, 247, 0.22));
  color: #f8fbff;
  font-weight: 800;
  box-shadow: var(--w40-glow);
}

.stTextInput input,
.stTextArea textarea,
div[data-baseweb="select"] > div,
div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
  border-color: rgba(99, 230, 255, 0.22);
  background-color: rgba(7, 10, 22, 0.72);
  color: var(--w40-text);
}

button[data-baseweb="tab"] {
  color: #b7c3e6;
  font-weight: 800;
}

button[data-baseweb="tab"][aria-selected="true"] {
  color: #ffffff;
  border-bottom-color: var(--w40-cyan);
}

/* RAG output */
.w40-mode-line {
  display: inline-flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 8px 0 18px;
}

/* responsive */
@media (max-width: 900px) {
  .w40-hero {
    grid-template-columns: 1fr;
    padding: 28px;
  }

  .w40-orb-stage {
    min-height: 240px;
  }

  div[data-testid="stMetric"] {
    min-height: auto;
  }
}

@media (prefers-reduced-motion: reduce) {
  .w40-orb,
  .w40-orb::before,
  .w40-orb::after {
    animation: none;
  }
}
</style>
""".strip()


def badge(label: object) -> str:
    return f'<span class="w40-status-badge">{html.escape(str(label))}</span>'


def paragraph(text: object) -> str:
    return html.escape(str(text)).replace("\n", "<br>")

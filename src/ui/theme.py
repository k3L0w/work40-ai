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
  padding: clamp(1.6rem, 2.8vw, 2.45rem) clamp(1.25rem, 3vw, 2.25rem) 3.5rem;
}

.block-container [data-testid="stVerticalBlock"] {
  gap: clamp(0.85rem, 1.4vw, 1.15rem);
}

.block-container [data-testid="stHorizontalBlock"] {
  gap: clamp(1rem, 1.8vw, 1.45rem);
  margin-bottom: clamp(0.35rem, 1vw, 0.75rem);
}

[role="tabpanel"] {
  padding-top: clamp(1rem, 1.8vw, 1.4rem);
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

.w40-hero-content {
  position: relative;
  z-index: 1;
}

.w40-orb-stage {
  display: grid;
  min-height: 330px;
  place-items: center;
  overflow: visible;
}

.w40-orb-shell {
  position: relative;
  width: min(340px, 74vw);
  aspect-ratio: 1;
  transform-style: preserve-3d;
  animation: w40-orb-float 12s ease-in-out infinite;
}

.w40-orb-halo {
  position: absolute;
  inset: -18%;
  border-radius: 999px;
  background:
    radial-gradient(circle, rgba(99, 230, 255, 0.22), transparent 58%),
    radial-gradient(circle at 64% 36%, rgba(168, 85, 247, 0.2), transparent 46%),
    radial-gradient(circle at 34% 70%, rgba(255, 77, 109, 0.12), transparent 42%);
  filter: blur(18px);
  opacity: 0.86;
  animation: w40-aura-breathe 12s ease-in-out infinite alternate;
}

.w40-orb,
.w40-orb-surface,
.w40-orb-grid,
.w40-orb-core,
.w40-orb-scan,
.w40-orb-ring,
.w40-orb-particles,
.w40-orb-particle {
  position: absolute;
}

.w40-orb {
  inset: 9%;
  overflow: hidden;
  border: 1px solid rgba(99, 230, 255, 0.44);
  border-radius: 999px;
  background:
    radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.82), transparent 0.17rem),
    radial-gradient(circle at 42% 36%, rgba(99, 230, 255, 0.8), transparent 4.8rem),
    radial-gradient(circle at 66% 60%, rgba(168, 85, 247, 0.72), transparent 5.8rem),
    radial-gradient(circle at 36% 70%, rgba(255, 77, 109, 0.36), transparent 5.4rem),
    radial-gradient(circle at 48% 58%, rgba(91, 140, 255, 0.54), transparent 7rem),
    rgba(10, 17, 38, 0.92);
  box-shadow:
    0 0 70px rgba(99, 230, 255, 0.28),
    0 0 115px rgba(168, 85, 247, 0.22),
    inset 0 0 58px rgba(99, 230, 255, 0.18),
    inset -26px -22px 64px rgba(3, 7, 18, 0.5);
  animation: w40-orb-breathe 18s ease-in-out infinite;
}

.w40-orb-surface {
  inset: -14%;
  border-radius: inherit;
  background:
    conic-gradient(from 0deg, transparent 0 14%, rgba(99, 230, 255, 0.24) 18%, transparent 25% 44%, rgba(168, 85, 247, 0.22) 52%, transparent 60% 78%, rgba(255, 77, 109, 0.16) 86%, transparent 94%),
    radial-gradient(circle at 28% 32%, rgba(255, 255, 255, 0.28), transparent 14%),
    radial-gradient(circle at 72% 66%, rgba(99, 230, 255, 0.2), transparent 18%);
  opacity: 0.58;
  mix-blend-mode: screen;
  transform: rotate(0deg) scale(1.08);
  animation: w40-orb-rotate 24s linear infinite;
}

.w40-orb-grid {
  inset: -5%;
  border-radius: inherit;
  opacity: 0.36;
  background:
    linear-gradient(90deg, transparent 48%, rgba(99, 230, 255, 0.42) 49% 51%, transparent 52%),
    linear-gradient(transparent 48%, rgba(168, 85, 247, 0.32) 49% 51%, transparent 52%);
  background-size: 38px 38px;
  transform: rotate(12deg) scale(1.08);
  animation: w40-grid-drift 30s linear infinite reverse;
}

.w40-orb-core {
  inset: 34%;
  border-radius: 999px;
  background:
    radial-gradient(circle, rgba(255, 255, 255, 0.96), rgba(99, 230, 255, 0.86) 26%, rgba(168, 85, 247, 0.36) 58%, transparent 72%);
  box-shadow:
    0 0 24px rgba(255, 255, 255, 0.54),
    0 0 58px rgba(99, 230, 255, 0.54),
    0 0 92px rgba(168, 85, 247, 0.4);
  animation: w40-core-pulse 6s ease-in-out infinite;
}

.w40-orb-scan {
  inset: 0;
  border-radius: inherit;
  background: linear-gradient(180deg, transparent 0 42%, rgba(255, 255, 255, 0.22) 48%, transparent 56%);
  mix-blend-mode: screen;
  opacity: 0.38;
  animation: w40-scan 12s ease-in-out infinite;
}

.w40-orb-ring {
  inset: 4%;
  border: 1px solid rgba(99, 230, 255, 0.48);
  border-radius: 999px;
  box-shadow: 0 0 34px rgba(99, 230, 255, 0.24);
  transform-style: preserve-3d;
}

.w40-orb-ring-1 {
  transform: rotateX(68deg) rotateZ(0deg);
  animation: w40-ring-one 12s linear infinite;
}

.w40-orb-ring-2 {
  inset: 0;
  border-color: rgba(168, 85, 247, 0.36);
  transform: rotateX(58deg) rotateY(26deg) rotateZ(90deg);
  animation: w40-ring-two 18s linear infinite reverse;
}

.w40-orb-ring-3 {
  inset: 15%;
  border-color: rgba(91, 140, 255, 0.35);
  transform: rotateX(76deg) rotateY(-18deg) rotateZ(35deg);
  animation: w40-ring-three 24s linear infinite;
}

.w40-orb-ring-4 {
  inset: -6%;
  border-color: rgba(255, 77, 109, 0.2);
  transform: rotateX(72deg) rotateY(12deg) rotateZ(120deg);
  animation: w40-ring-four 30s linear infinite reverse;
}

.w40-orb-particles {
  inset: -8%;
  pointer-events: none;
}

.w40-orb-particle {
  width: var(--spark-size, 5px);
  height: var(--spark-size, 5px);
  border-radius: 999px;
  background: var(--spark-color, var(--w40-cyan));
  box-shadow: 0 0 18px currentColor;
  color: var(--spark-color, var(--w40-cyan));
  left: var(--spark-x);
  top: var(--spark-y);
  opacity: 0.55;
  animation: w40-particle-drift var(--spark-duration, 7s) ease-in-out var(--spark-delay, 0s) infinite alternate;
}

.w40-orb-particle-1 { --spark-x: 8%; --spark-y: 30%; --spark-size: 4px; --spark-duration: 6.8s; --spark-delay: -0.7s; --spark-color: #63e6ff; }
.w40-orb-particle-2 { --spark-x: 16%; --spark-y: 68%; --spark-size: 6px; --spark-duration: 8.9s; --spark-delay: -2.1s; --spark-color: #a855f7; }
.w40-orb-particle-3 { --spark-x: 28%; --spark-y: 12%; --spark-size: 3px; --spark-duration: 7.6s; --spark-delay: -1.4s; --spark-color: #5b8cff; }
.w40-orb-particle-4 { --spark-x: 44%; --spark-y: 4%; --spark-size: 5px; --spark-duration: 10.2s; --spark-delay: -3.3s; --spark-color: #ff4d6d; }
.w40-orb-particle-5 { --spark-x: 64%; --spark-y: 10%; --spark-size: 4px; --spark-duration: 8.1s; --spark-delay: -4.8s; --spark-color: #63e6ff; }
.w40-orb-particle-6 { --spark-x: 82%; --spark-y: 28%; --spark-size: 6px; --spark-duration: 9.7s; --spark-delay: -1.8s; --spark-color: #a855f7; }
.w40-orb-particle-7 { --spark-x: 91%; --spark-y: 52%; --spark-size: 3px; --spark-duration: 7.2s; --spark-delay: -5.2s; --spark-color: #5b8cff; }
.w40-orb-particle-8 { --spark-x: 76%; --spark-y: 78%; --spark-size: 5px; --spark-duration: 11.4s; --spark-delay: -2.7s; --spark-color: #63e6ff; }
.w40-orb-particle-9 { --spark-x: 58%; --spark-y: 90%; --spark-size: 4px; --spark-duration: 8.5s; --spark-delay: -6.1s; --spark-color: #ff4d6d; }
.w40-orb-particle-10 { --spark-x: 36%; --spark-y: 86%; --spark-size: 6px; --spark-duration: 9.1s; --spark-delay: -0.9s; --spark-color: #a855f7; }
.w40-orb-particle-11 { --spark-x: 10%; --spark-y: 48%; --spark-size: 3px; --spark-duration: 10.8s; --spark-delay: -4.4s; --spark-color: #63e6ff; }
.w40-orb-particle-12 { --spark-x: 88%; --spark-y: 68%; --spark-size: 4px; --spark-duration: 7.9s; --spark-delay: -3.8s; --spark-color: #5b8cff; }
.w40-orb-particle-13 { --spark-x: 24%; --spark-y: 28%; --spark-size: 4px; --spark-duration: 12.1s; --spark-delay: -2.5s; --spark-color: #ff4d6d; }
.w40-orb-particle-14 { --spark-x: 68%; --spark-y: 42%; --spark-size: 3px; --spark-duration: 6.9s; --spark-delay: -5.6s; --spark-color: #63e6ff; }

@keyframes w40-orb-float {
  0%, 100% { transform: translate3d(0, 0, 0) rotateZ(-1deg); }
  28% { transform: translate3d(7px, -10px, 0) rotateZ(1.2deg); }
  63% { transform: translate3d(-6px, 5px, 0) rotateZ(-0.8deg); }
}

@keyframes w40-aura-breathe {
  from { opacity: 0.48; transform: scale(0.92); filter: blur(18px); }
  to { opacity: 1; transform: scale(1.1); filter: blur(26px); }
}

@keyframes w40-orb-breathe {
  0%, 100% { filter: saturate(1) brightness(1); transform: scale(1); }
  50% { filter: saturate(1.22) brightness(1.12); transform: scale(1.025); }
}

@keyframes w40-orb-rotate {
  to { transform: rotate(360deg) scale(1.08); }
}

@keyframes w40-grid-drift {
  to { transform: rotate(372deg) scale(1.08); }
}

@keyframes w40-core-pulse {
  0%, 100% { opacity: 0.72; transform: scale(0.82); box-shadow: 0 0 20px rgba(99, 230, 255, 0.42), 0 0 54px rgba(168, 85, 247, 0.34); }
  48% { opacity: 1; transform: scale(1.28); box-shadow: 0 0 34px rgba(255, 255, 255, 0.62), 0 0 78px rgba(99, 230, 255, 0.68), 0 0 118px rgba(168, 85, 247, 0.5); }
  72% { opacity: 0.9; transform: scale(1.04); }
}

@keyframes w40-scan {
  0%, 100% { transform: translateY(-42%); opacity: 0.14; }
  48% { transform: translateY(44%); opacity: 0.42; }
}

@keyframes w40-ring-one {
  to { transform: rotateX(68deg) rotateZ(360deg); }
}

@keyframes w40-ring-two {
  to { transform: rotateX(58deg) rotateY(26deg) rotateZ(450deg); }
}

@keyframes w40-ring-three {
  to { transform: rotateX(76deg) rotateY(-18deg) rotateZ(395deg); }
}

@keyframes w40-ring-four {
  to { transform: rotateX(72deg) rotateY(12deg) rotateZ(480deg); }
}

@keyframes w40-particle-drift {
  0% { transform: translate3d(-10px, 8px, 0) scale(0.72); opacity: 0.18; }
  42% { transform: translate3d(14px, -16px, 0) scale(1.18); opacity: 0.88; }
  100% { transform: translate3d(-12px, -24px, 0) scale(0.86); opacity: 0.38; }
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
  padding: clamp(1.1rem, 1.6vw, 1.35rem);
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
  margin: 14px 0 28px;
  color: #c8d5f7;
}

.w40-glass-card,
.w40-answer-card,
.w40-source-card {
  padding: clamp(1.1rem, 1.65vw, 1.4rem);
}

.w40-answer-card {
  max-width: 920px;
  margin-bottom: clamp(0.9rem, 1.4vw, 1.15rem);
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
  gap: clamp(0.95rem, 1.6vw, 1.25rem);
  margin-top: 0.35rem;
}

.w40-source-meta {
  color: #91a3d7;
  font-size: 0.82rem;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
  padding: clamp(1rem, 1.5vw, 1.25rem);
  margin-bottom: clamp(0.75rem, 1.25vw, 1rem);
}

.w40-source-card {
  margin-bottom: 0.25rem;
}

/* sidebar */
[data-testid="stSidebar"] {
  background:
    radial-gradient(circle at 30% 10%, rgba(168, 85, 247, 0.22), transparent 16rem),
    linear-gradient(180deg, #080b18 0%, #0c1022 100%);
  border-right: 1px solid rgba(99, 230, 255, 0.16);
}

[data-testid="stSidebarContent"] {
  padding: 1.15rem 1.15rem 1.6rem;
}

[data-testid="stSidebarContent"] [data-testid="stVerticalBlock"] {
  gap: 0.85rem;
}

[data-testid="stSidebarContent"] hr {
  margin: 1.15rem 0;
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
  padding: 16px 16px 14px;
  margin-bottom: 16px;
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

  .block-container {
    padding-inline: 1rem;
  }

  .w40-orb-stage {
    min-height: 270px;
  }

  .w40-orb-shell {
    width: min(290px, 76vw);
  }

  div[data-testid="stMetric"] {
    min-height: auto;
  }
}

@media (prefers-reduced-motion: reduce) {
  .w40-orb-shell,
  .w40-orb-halo,
  .w40-orb,
  .w40-orb-surface,
  .w40-orb-grid,
  .w40-orb-core,
  .w40-orb-scan,
  .w40-orb-ring,
  .w40-orb-particle {
    animation: none;
  }

  .w40-orb-particle {
    opacity: 0.35;
  }
}
</style>
""".strip()


def badge(label: object) -> str:
    return f'<span class="w40-status-badge">{html.escape(str(label))}</span>'


def paragraph(text: object) -> str:
    return html.escape(str(text)).replace("\n", "<br>")

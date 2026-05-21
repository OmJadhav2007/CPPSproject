DARK_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap');

/* ── Root & Base ── */
:root {
    --bg-primary: #0a0b0f;
    --bg-secondary: #111318;
    --bg-card: #16181f;
    --bg-glass: rgba(255,255,255,0.04);
    --border: rgba(255,255,255,0.08);
    --border-glow: rgba(139,92,246,0.3);
    --accent: #8b5cf6;
    --accent-2: #06b6d4;
    --accent-3: #f59e0b;
    --accent-4: #10b981;
    --accent-5: #f43f5e;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #475569;
    --gradient-1: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
    --gradient-2: linear-gradient(135deg, #f59e0b 0%, #f43f5e 100%);
    --gradient-3: linear-gradient(135deg, #10b981 0%, #06b6d4 100%);
    --shadow: 0 4px 24px rgba(0,0,0,0.4);
    --shadow-glow: 0 0 30px rgba(139,92,246,0.15);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* ── Hide Streamlit Defaults ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 1.5rem 2rem !important;
    max-width: 1400px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
    min-width: 240px !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
}

/* ── Metric Cards ── */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    border-color: var(--border-glow);
    box-shadow: var(--shadow-glow);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--gradient-1);
}
.metric-card.green::before { background: var(--gradient-3); }
.metric-card.amber::before { background: linear-gradient(135deg,#f59e0b,#fbbf24); }
.metric-card.pink::before { background: var(--gradient-2); }

.metric-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.4rem;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1;
}
.metric-sub {
    font-size: 0.75rem;
    color: var(--text-secondary);
    margin-top: 0.35rem;
}

/* ── Page Title ── */
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
}
.page-subtitle {
    font-size: 0.9rem;
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(139,92,246,0.15) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--gradient-1) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.25rem !important;
    transition: opacity 0.2s, transform 0.15s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
}

/* ── Checkbox ── */
.stCheckbox > label {
    color: var(--text-primary) !important;
}
.stCheckbox > label > div[data-testid="stCheckbox"] > div {
    border-color: var(--accent) !important;
}

/* ── Dataframe ── */
.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* ── Goal Card ── */
.goal-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.goal-card:hover {
    border-color: rgba(139,92,246,0.4);
    box-shadow: 0 2px 16px rgba(139,92,246,0.1);
}
.goal-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1rem; }
.goal-meta { font-size: 0.78rem; color: var(--text-secondary); margin-top: 0.2rem; }

/* ── Badge ── */
.badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.badge-study { background: rgba(6,182,212,0.15); color: #06b6d4; }
.badge-fitness { background: rgba(16,185,129,0.15); color: #10b981; }
.badge-productivity { background: rgba(139,92,246,0.15); color: #a78bfa; }
.badge-health { background: rgba(244,63,94,0.15); color: #fb7185; }
.badge-reading { background: rgba(245,158,11,0.15); color: #fbbf24; }
.badge-coding { background: rgba(59,130,246,0.15); color: #60a5fa; }
.badge-custom { background: rgba(255,255,255,0.08); color: #94a3b8; }

/* ── Priority ── */
.priority-high { color: #f43f5e; font-weight: 700; }
.priority-medium { color: #f59e0b; font-weight: 600; }
.priority-low { color: #10b981; font-weight: 600; }

/* ── Tracker Table ── */
.tracker-header {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
}
.week-label {
    background: rgba(139,92,246,0.12);
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 8px;
    padding: 0.25rem 0.75rem;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--accent);
    display: inline-block;
    margin-bottom: 0.5rem;
}

/* ── Calendar ── */
.cal-day {
    width: 36px; height: 36px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.82rem; font-weight: 600;
    cursor: pointer;
    transition: transform 0.15s;
}
.cal-day:hover { transform: scale(1.1); }
.cal-complete { background: rgba(16,185,129,0.25); color: #10b981; border: 1px solid rgba(16,185,129,0.3); }
.cal-partial { background: rgba(245,158,11,0.2); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }
.cal-missed { background: rgba(244,63,94,0.15); color: #f43f5e; border: 1px solid rgba(244,63,94,0.2); }
.cal-future { background: var(--bg-glass); color: var(--text-muted); }
.cal-none { background: var(--bg-glass); color: var(--text-muted); }
.cal-today { border: 2px solid var(--accent) !important; }

/* ── Note Card ── */
.note-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
}
.note-title { font-family: 'Syne', sans-serif; font-weight: 700; }
.note-date { font-size: 0.72rem; color: var(--text-muted); }

/* ── Sidebar Nav ── */
.nav-logo {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    padding: 0.5rem 0;
}
.nav-user {
    font-size: 0.8rem;
    color: var(--text-secondary);
    padding: 0.25rem 0 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}

/* ── Dividers ── */
hr { border-color: var(--border) !important; }

/* ── Plotly Charts ── */
.js-plotly-plot { border-radius: 12px; overflow: hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* ── Animations ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}
.animate-in { animation: fadeInUp 0.35s ease forwards; }

/* ── Radio Tabs ── */
.stRadio > div { flex-direction: row !important; gap: 0.5rem; }
.stRadio > div > label {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 0.35rem 0.9rem !important;
    cursor: pointer;
    transition: border-color 0.2s;
    font-size: 0.85rem !important;
}
</style>
"""

MOTTOS = [
    "🚀 Ready to level up today?",
    "✦ One step closer to your goals.",
    "🏗️ Build your future one day at a time.",
    "⚡ Stay consistent. Stay unstoppable.",
    "📈 Progress starts here.",
]

CATEGORY_COLORS = {
    "Study": "#06b6d4",
    "Fitness": "#10b981",
    "Productivity": "#8b5cf6",
    "Health": "#f43f5e",
    "Reading": "#f59e0b",
    "Coding": "#3b82f6",
    "Custom": "#94a3b8",
}

CATEGORY_EMOJIS = {
    "Study": "📚",
    "Fitness": "💪",
    "Productivity": "⚡",
    "Health": "❤️",
    "Reading": "📖",
    "Coding": "💻",
    "Custom": "🎯",
}

PRIORITY_COLORS = {
    "High": "#f43f5e",
    "Medium": "#f59e0b",
    "Low": "#10b981",
}

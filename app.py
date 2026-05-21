import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import date
import random
from frontend.components.api_client import api_get
from frontend.components.styles import MOTTOS, CATEGORY_COLORS, CATEGORY_EMOJIS

def render():
    user = st.session_state.get("user", {})
    username = user.get("username", "User")

    motto = random.choice(MOTTOS) if not st.session_state.get("motto") else st.session_state["motto"]
    st.session_state["motto"] = motto

    st.markdown(f'<div class="page-title">{motto}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">Welcome back, <strong>{username}</strong> — here\'s your progress overview.</div>', unsafe_allow_html=True)

    # Fetch stats
    stats = api_get("/api/progress/dashboard-stats") or {}
    goals = api_get("/api/goals/", params={"is_active": "true"}) or []

    # ── KPI Cards ──
    col1, col2, col3, col4, col5 = st.columns(5)
    kpis = [
        ("col1", "TOTAL GOALS", stats.get("total_goals", 0), "goals tracked", "", ""),
        ("col2", "DONE TODAY", stats.get("completed_today", 0), "tasks completed", "green", ""),
        ("col3", "WEEKLY %", f"{stats.get('weekly_completion_pct', 0)}%", "completion rate", "amber", ""),
        ("col4", "🔥 STREAK", stats.get("total_streak", 0), "combined days", "pink", ""),
        ("col5", "ALL TIME", stats.get("total_completions", 0), "total completions", "green", ""),
    ]
    for col, label, val, sub, color, _ in zip(
        [col1, col2, col3, col4, col5], kpis[0::1]
    ):
        _, label, val, sub, color, __ = kpis.pop(0)
        with col:
            st.markdown(f"""
            <div class="metric-card {color} animate-in">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Analytics row ──
    analytics = api_get("/api/progress/analytics") or {}
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<div class="metric-label" style="margin-bottom:0.75rem;">WEEKLY COMPLETION TREND</div>', unsafe_allow_html=True)
        weekly = analytics.get("weekly", {})
        if weekly:
            weeks = sorted(weekly.keys())
            pcts = [round(weekly[w]["completed"] / weekly[w]["total"] * 100, 1) if weekly[w]["total"] > 0 else 0 for w in weeks]
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=weeks, y=pcts,
                fill="tozeroy",
                fillcolor="rgba(139,92,246,0.12)",
                line=dict(color="#8b5cf6", width=2.5),
                mode="lines+markers",
                marker=dict(size=7, color="#8b5cf6", line=dict(width=2, color="#fff")),
                name="Completion %"
            ))
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans", color="#94a3b8", size=12),
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)", showgrid=True),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)", showgrid=True, range=[0, 105], ticksuffix="%"),
                height=220,
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown('<div style="color:#475569;font-size:0.85rem;text-align:center;padding:2rem;">Start tracking to see your trends!</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="metric-label" style="margin-bottom:0.75rem;">GOAL CATEGORIES</div>', unsafe_allow_html=True)
        cat_data = analytics.get("categories", {})
        if cat_data:
            labels = list(cat_data.keys())
            values = [cat_data[c].get("completed", 0) for c in labels]
            colors_list = [CATEGORY_COLORS.get(l, "#94a3b8") for l in labels]
            fig2 = go.Figure(go.Pie(
                labels=labels, values=values,
                hole=0.6,
                marker=dict(colors=colors_list, line=dict(color="#111318", width=2)),
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>%{value} completed<extra></extra>",
            ))
            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans", color="#94a3b8"),
                margin=dict(l=0, r=0, t=0, b=0),
                showlegend=True,
                legend=dict(font=dict(size=11, color="#94a3b8"), bgcolor="rgba(0,0,0,0)"),
                height=220
            )
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown('<div style="color:#475569;font-size:0.85rem;text-align:center;padding:2rem;">No category data yet</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Active Goals ──
    col_goals, col_streaks = st.columns([3, 2])

    with col_goals:
        st.markdown('<div class="metric-label" style="margin-bottom:0.75rem;">ACTIVE GOALS</div>', unsafe_allow_html=True)
        if goals:
            for goal in goals[:5]:
                cat = goal.get("category", "Custom")
                emoji = CATEGORY_EMOJIS.get(cat, "🎯")
                color = CATEGORY_COLORS.get(cat, "#94a3b8")
                priority = goal.get("priority", "Medium")
                p_color = {"High": "#f43f5e", "Medium": "#f59e0b", "Low": "#10b981"}.get(priority, "#94a3b8")
                st.markdown(f"""
                <div class="goal-card animate-in">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="font-size:1.1rem;">{emoji}</span>
                            <span class="goal-title" style="margin-left:0.5rem;">{goal['title']}</span>
                        </div>
                        <span style="font-size:0.72rem;font-weight:700;color:{p_color};">{priority}</span>
                    </div>
                    <div class="goal-meta">
                        <span style="color:{color};font-weight:600;">{cat}</span> &nbsp;·&nbsp; {goal.get('target_frequency','Daily')}
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div style="color:#475569;text-align:center;padding:1.5rem;">No active goals. Create one to get started! ✨</div>', unsafe_allow_html=True)

    with col_streaks:
        st.markdown('<div class="metric-label" style="margin-bottom:0.75rem;">🔥 STREAKS</div>', unsafe_allow_html=True)
        streaks = analytics.get("streaks", [])
        if streaks:
            streak_goals = [s["goal"] for s in streaks[:6]]
            streak_vals = [s["current"] for s in streaks[:6]]
            fig3 = go.Figure(go.Bar(
                x=streak_vals, y=streak_goals,
                orientation="h",
                marker=dict(
                    color=streak_vals,
                    colorscale=[[0, "#f43f5e"], [0.5, "#f59e0b"], [1, "#10b981"]],
                    line=dict(width=0)
                ),
                text=[f"{v}d" for v in streak_vals],
                textposition="inside",
                textfont=dict(color="white", family="DM Sans", size=11)
            ))
            fig3.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans", color="#94a3b8", size=11),
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False),
                height=220,
                showlegend=False
            )
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown("""
            <div style="background:rgba(139,92,246,0.08);border:1px solid rgba(139,92,246,0.2);border-radius:12px;padding:1.5rem;text-align:center;">
                <div style="font-size:2rem;">🔥</div>
                <div style="color:#94a3b8;font-size:0.85rem;margin-top:0.5rem;">Complete goals daily to build streaks!</div>
            </div>""", unsafe_allow_html=True)

    # ── Achievement Badges ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="metric-label" style="margin-bottom:0.75rem;">ACHIEVEMENTS</div>', unsafe_allow_html=True)
    total_done = stats.get("total_completions", 0)
    total_g = stats.get("total_goals", 0)
    streak_total = stats.get("total_streak", 0)

    badges = [
        ("🎯", "Goal Setter", "Created first goal", total_g >= 1),
        ("✅", "First Step", "Completed first task", total_done >= 1),
        ("🔥", "On Fire", "5+ day streak", streak_total >= 5),
        ("💎", "Diamond Habit", "50+ completions", total_done >= 50),
        ("🏆", "Champion", "100+ completions", total_done >= 100),
        ("⚡", "Powerhouse", "10+ active goals", total_g >= 10),
    ]
    b_cols = st.columns(6)
    for col, (emoji, name, desc, earned) in zip(b_cols, badges):
        with col:
            opacity = "1" if earned else "0.3"
            glow = "rgba(139,92,246,0.2)" if earned else "transparent"
            st.markdown(f"""
            <div style="background:{glow};border:1px solid {'rgba(139,92,246,0.3)' if earned else 'rgba(255,255,255,0.06)'};
                border-radius:12px;padding:0.75rem;text-align:center;opacity:{opacity};transition:all 0.2s;">
                <div style="font-size:1.6rem;">{emoji}</div>
                <div style="font-size:0.7rem;font-weight:700;color:#f1f5f9;margin-top:0.3rem;">{name}</div>
                <div style="font-size:0.62rem;color:#64748b;margin-top:0.1rem;">{desc}</div>
            </div>""", unsafe_allow_html=True)

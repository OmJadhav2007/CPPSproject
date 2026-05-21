import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from frontend.components.api_client import api_get
from frontend.components.styles import CATEGORY_COLORS

def render():
    st.markdown('<div class="page-title">Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Deep insights from your real data — powered by your consistency.</div>', unsafe_allow_html=True)

    analytics = api_get("/api/progress/analytics") or {}
    stats = api_get("/api/progress/dashboard-stats") or {}

    # Summary KPIs
    k1, k2, k3, k4 = st.columns(4)
    kpi_data = [
        (k1, "TOTAL COMPLETIONS", stats.get("total_completions", 0), "#8b5cf6"),
        (k2, "WEEKLY RATE", f"{stats.get('weekly_completion_pct', 0)}%", "#06b6d4"),
        (k3, "CURRENT STREAK", stats.get("total_streak", 0), "#f59e0b"),
        (k4, "ACTIVE GOALS", stats.get("active_goals", 0), "#10b981"),
    ]
    for col, label, val, color in kpi_data:
        with col:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                border-radius:14px;padding:1.1rem 1.25rem;border-top:2px solid {color};">
                <div style="font-size:0.68rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#475569;">{label}</div>
                <div style="font-family:'Syne',sans-serif;font-size:1.9rem;font-weight:800;color:{color};margin-top:0.3rem;">{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 1: Weekly Bar + Category Radar ──
    row1_left, row1_right = st.columns(2)

    with row1_left:
        st.markdown('<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.1em;color:#475569;text-transform:uppercase;margin-bottom:0.75rem;">WEEKLY COMPLETION BARS</div>', unsafe_allow_html=True)
        weekly = analytics.get("weekly", {})
        if weekly:
            weeks = sorted(weekly.keys())
            completed = [weekly[w]["completed"] for w in weeks]
            total = [weekly[w]["total"] for w in weeks]
            pcts = [round(c / t * 100, 1) if t > 0 else 0 for c, t in zip(completed, total)]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=weeks, y=total,
                name="Total",
                marker_color="rgba(255,255,255,0.06)",
                marker_line_width=0
            ))
            fig.add_trace(go.Bar(
                x=weeks, y=completed,
                name="Completed",
                marker=dict(
                    color=pcts,
                    colorscale=[[0, "#f43f5e"], [0.5, "#f59e0b"], [1, "#10b981"]],
                    line_width=0
                ),
                text=[f"{p}%" for p in pcts],
                textposition="outside",
                textfont=dict(size=10, color="#94a3b8")
            ))
            fig.update_layout(
                barmode="overlay",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans", color="#94a3b8", size=11),
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
                height=280
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No weekly data yet.")

    with row1_right:
        st.markdown('<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.1em;color:#475569;text-transform:uppercase;margin-bottom:0.75rem;">CATEGORY PERFORMANCE</div>', unsafe_allow_html=True)
        cat_data = analytics.get("categories", {})
        if cat_data:
            cats = list(cat_data.keys())
            pcts = [round(cat_data[c]["completed"] / cat_data[c]["total"] * 100, 1) if cat_data[c]["total"] > 0 else 0 for c in cats]
            colors = [CATEGORY_COLORS.get(c, "#94a3b8") for c in cats]

            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=cats, y=pcts,
                marker=dict(color=colors, line_width=0),
                text=[f"{p}%" for p in pcts],
                textposition="outside",
                textfont=dict(size=10, color="#94a3b8")
            ))
            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans", color="#94a3b8", size=11),
                margin=dict(l=10, r=10, t=30, b=10),
                xaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.04)", range=[0, 110], ticksuffix="%"),
                height=280,
                showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No category data yet.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2: Productivity Heatmap + Streak Chart ──
    row2_left, row2_right = st.columns(2)

    with row2_left:
        st.markdown('<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.1em;color:#475569;text-transform:uppercase;margin-bottom:0.75rem;">PRODUCTIVITY HEATMAP</div>', unsafe_allow_html=True)
        heatmap = analytics.get("heatmap", {})
        if heatmap:
            from datetime import datetime
            dates = sorted(heatmap.keys())
            x_vals, y_vals, z_vals = [], [], []
            for d in dates:
                try:
                    dt = datetime.strptime(d, "%Y-%m-%d")
                    x_vals.append(dt.strftime("%Y-W%W"))
                    y_vals.append(dt.strftime("%a"))
                    z_vals.append(heatmap[d])
                except:
                    pass

            if x_vals:
                fig3 = go.Figure(go.Scatter(
                    x=x_vals, y=y_vals,
                    mode="markers",
                    marker=dict(
                        size=[max(8, v * 8) for v in z_vals],
                        color=z_vals,
                        colorscale=[[0, "#1e293b"], [0.01, "#7c3aed"], [1, "#10b981"]],
                        line=dict(width=0),
                        showscale=True,
                        colorbar=dict(
                            thickness=10,
                            len=0.8,
                            tickfont=dict(color="#94a3b8", size=10),
                            bgcolor="rgba(0,0,0,0)"
                        )
                    ),
                    text=[f"{d}: {v} completed" for d, v in zip(dates, z_vals)],
                    hovertemplate="%{text}<extra></extra>"
                ))
                fig3.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="DM Sans", color="#94a3b8", size=11),
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=280
                )
                st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("No heatmap data yet.")
        else:
            st.info("Track some goals to see heatmap data!")

    with row2_right:
        st.markdown('<div style="font-size:0.72rem;font-weight:700;letter-spacing:0.1em;color:#475569;text-transform:uppercase;margin-bottom:0.75rem;">STREAK LEADERS</div>', unsafe_allow_html=True)
        streaks = analytics.get("streaks", [])
        if streaks:
            top = sorted(streaks, key=lambda x: x["longest"], reverse=True)[:8]
            names = [s["goal"][:20] for s in top]
            current_s = [s["current"] for s in top]
            longest_s = [s["longest"] for s in top]

            fig4 = go.Figure()
            fig4.add_trace(go.Bar(
                name="Longest Streak",
                x=names, y=longest_s,
                marker_color="rgba(139,92,246,0.3)",
                marker_line_width=0
            ))
            fig4.add_trace(go.Bar(
                name="Current Streak",
                x=names, y=current_s,
                marker=dict(
                    color=current_s,
                    colorscale=[[0, "#f43f5e"], [0.5, "#f59e0b"], [1, "#10b981"]],
                    line_width=0
                )
            ))
            fig4.update_layout(
                barmode="overlay",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans", color="#94a3b8", size=11),
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickangle=-30),
                yaxis=dict(gridcolor="rgba(255,255,255,0.04)"),
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
                height=280
            )
            st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Build streaks to see your leaders!")

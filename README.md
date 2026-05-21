import streamlit as st
from datetime import date, timedelta
from frontend.components.api_client import api_get, api_post
from frontend.components.styles import CATEGORY_EMOJIS, CATEGORY_COLORS

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def get_date_for_week_day(week_number: int, day_idx: int) -> date:
    """Calculate the actual date for a given week number and day index."""
    today = date.today()
    # Week 1 starts from the Monday of the current month's first week
    from calendar import monthrange
    year, month = today.year, today.month
    first_day = date(year, month, 1)
    # Get Monday of the first week
    first_monday = first_day - timedelta(days=first_day.weekday())
    target = first_monday + timedelta(weeks=week_number - 1, days=day_idx)
    return target

def render():
    st.markdown('<div class="page-title">Weekly Tracker</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Check off your daily goals — every click saves instantly.</div>', unsafe_allow_html=True)

    goals = api_get("/api/goals/", params={"is_active": "true"}) or []

    if not goals:
        st.markdown("""
        <div style="background:rgba(139,92,246,0.06);border:1px dashed rgba(139,92,246,0.25);
            border-radius:14px;padding:3rem;text-align:center;">
            <div style="font-size:3rem;margin-bottom:0.75rem;">📋</div>
            <div style="color:#94a3b8;font-size:1rem;">Create some goals first to start tracking!</div>
        </div>""", unsafe_allow_html=True)
        return

    # Fetch ALL progress
    all_progress = api_get("/api/progress/") or []
    # Build lookup: (goal_id, week_number, day) -> completed bool
    progress_map = {}
    for p in all_progress:
        key = (p["goal_id"], p["week_number"], p["day_of_week"])
        progress_map[key] = p["completed"]

    today = date.today()

    # Week selector
    col_ws, col_ws2 = st.columns([2, 4])
    with col_ws:
        week_view = st.radio(
            "View",
            ["Week 1", "Week 2", "Week 3", "Week 4", "All 4 Weeks"],
            horizontal=True,
            label_visibility="collapsed"
        )

    if week_view == "All 4 Weeks":
        weeks_to_show = [1, 2, 3, 4]
    else:
        weeks_to_show = [int(week_view.split()[1])]

    st.markdown("<br>", unsafe_allow_html=True)

    for week_num in weeks_to_show:
        st.markdown(f'<div class="week-label">WEEK {week_num}</div>', unsafe_allow_html=True)

        # Header row
        header_cols = st.columns([3] + [1] * 7)
        with header_cols[0]:
            st.markdown('<div class="tracker-header" style="padding:0.5rem 0;">GOAL</div>', unsafe_allow_html=True)
        for i, day in enumerate(DAYS):
            day_date = get_date_for_week_day(week_num, i)
            is_today = day_date == today
            with header_cols[i + 1]:
                color = "#8b5cf6" if is_today else "#475569"
                st.markdown(f'<div class="tracker-header" style="text-align:center;padding:0.5rem 0;color:{color};">{day}<br><span style="font-size:0.65rem;font-weight:400;">{day_date.strftime("%d")}</span></div>', unsafe_allow_html=True)

        st.markdown('<hr style="margin:0.25rem 0 0.5rem;">', unsafe_allow_html=True)

        # Goal rows
        for goal in goals:
            goal_id = goal["id"]
            cat = goal.get("category", "Custom")
            emoji = CATEGORY_EMOJIS.get(cat, "🎯")
            color = CATEGORY_COLORS.get(cat, "#94a3b8")

            row_cols = st.columns([3] + [1] * 7)
            with row_cols[0]:
                st.markdown(f"""
                <div style="padding:0.4rem 0;display:flex;align-items:center;gap:0.4rem;">
                    <span>{emoji}</span>
                    <span style="font-size:0.85rem;font-weight:600;color:#f1f5f9;">{goal['title'][:28]}{'…' if len(goal['title'])>28 else ''}</span>
                    <span style="font-size:0.68rem;color:{color};font-weight:600;">{cat}</span>
                </div>""", unsafe_allow_html=True)

            for i, day in enumerate(DAYS):
                key = (goal_id, week_num, day)
                current_val = progress_map.get(key, False)
                day_date = get_date_for_week_day(week_num, i)

                with row_cols[i + 1]:
                    cb_key = f"cb_{goal_id}_w{week_num}_{day}"
                    checked = st.checkbox(
                        label="",
                        value=current_val,
                        key=cb_key,
                        label_visibility="collapsed"
                    )
                    if checked != current_val:
                        # Save to backend immediately
                        result = api_post("/api/progress/checkbox", {
                            "goal_id": goal_id,
                            "week_number": week_num,
                            "day_of_week": day,
                            "completed": checked,
                            "date": str(day_date)
                        })
                        if result:
                            progress_map[key] = checked
                            st.rerun()

            # Row completion bar
            row_done = sum(1 for d in DAYS if progress_map.get((goal_id, week_num, d), False))
            pct = row_done / 7 * 100
            bar_color = "#10b981" if pct >= 80 else "#f59e0b" if pct >= 40 else "#f43f5e" if pct > 0 else "#1e293b"

            prog_col = st.columns([3, 7])
            with prog_col[1]:
                st.markdown(f"""
                <div style="height:3px;background:#1e293b;border-radius:2px;margin-bottom:0.5rem;">
                    <div style="height:100%;width:{pct}%;background:{bar_color};border-radius:2px;transition:width 0.3s;"></div>
                </div>""", unsafe_allow_html=True)

        # Week summary
        week_progress = {}
        for goal in goals:
            done = sum(1 for d in DAYS if progress_map.get((goal["id"], week_num, d), False))
            week_progress[goal["id"]] = done
        total_possible = len(goals) * 7
        total_done = sum(week_progress.values())
        week_pct = round(total_done / total_possible * 100) if total_possible > 0 else 0

        w_color = "#10b981" if week_pct >= 80 else "#f59e0b" if week_pct >= 40 else "#f43f5e"
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);
            border-radius:10px;padding:0.75rem 1rem;margin:0.5rem 0 1.5rem;
            display:flex;justify-content:space-between;align-items:center;">
            <span style="font-size:0.78rem;color:#64748b;font-weight:600;">WEEK {week_num} SUMMARY</span>
            <span style="font-size:0.9rem;font-weight:700;color:{w_color};">{total_done}/{total_possible} — {week_pct}%</span>
        </div>""", unsafe_allow_html=True)

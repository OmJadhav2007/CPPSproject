import streamlit as st
from datetime import date
import calendar as cal_lib
from frontend.components.api_client import api_get

MONTH_NAMES = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]

def render():
    st.markdown('<div class="page-title">Calendar</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Visualize your consistency over time.</div>', unsafe_allow_html=True)

    today = date.today()

    # Month/Year navigation
    if "cal_year" not in st.session_state:
        st.session_state.cal_year = today.year
    if "cal_month" not in st.session_state:
        st.session_state.cal_month = today.month

    nav1, nav2, nav3, nav4 = st.columns([1, 2, 1, 4])
    with nav1:
        if st.button("◀ Prev"):
            if st.session_state.cal_month == 1:
                st.session_state.cal_month = 12
                st.session_state.cal_year -= 1
            else:
                st.session_state.cal_month -= 1
            st.rerun()
    with nav2:
        st.markdown(f"""
        <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;
            background:linear-gradient(135deg,#8b5cf6,#06b6d4);-webkit-background-clip:text;
            -webkit-text-fill-color:transparent;text-align:center;padding:0.2rem 0;">
            {MONTH_NAMES[st.session_state.cal_month - 1]} {st.session_state.cal_year}
        </div>""", unsafe_allow_html=True)
    with nav3:
        if st.button("Next ▶"):
            if st.session_state.cal_month == 12:
                st.session_state.cal_month = 1
                st.session_state.cal_year += 1
            else:
                st.session_state.cal_month += 1
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Fetch calendar data
    cal_data = api_get("/api/progress/calendar", params={
        "year": st.session_state.cal_year,
        "month": st.session_state.cal_month
    }) or {}

    # Legend
    leg_cols = st.columns([1, 1, 1, 1, 4])
    legends = [
        ("#10b981", "rgba(16,185,129,0.15)", "Complete"),
        ("#f59e0b", "rgba(245,158,11,0.15)", "Partial"),
        ("#f43f5e", "rgba(244,63,94,0.1)", "Missed"),
    ]
    for col, (color, bg, label) in zip(leg_cols[:3], legends):
        with col:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:0.4rem;font-size:0.78rem;color:#94a3b8;">
                <div style="width:12px;height:12px;border-radius:3px;background:{bg};border:1px solid {color};"></div>
                {label}
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Day headers
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    header_cols = st.columns(7)
    for col, dn in zip(header_cols, day_names):
        with col:
            st.markdown(f'<div style="text-align:center;font-size:0.72rem;font-weight:700;color:#475569;letter-spacing:0.08em;padding-bottom:0.5rem;">{dn}</div>', unsafe_allow_html=True)

    # Build calendar grid
    year = st.session_state.cal_year
    month = st.session_state.cal_month
    first_weekday, days_in_month = cal_lib.monthrange(year, month)

    # Pad start (Monday-based)
    cells = [""] * first_weekday + list(range(1, days_in_month + 1))
    # Pad end to complete grid
    while len(cells) % 7 != 0:
        cells.append("")

    weeks = [cells[i:i+7] for i in range(0, len(cells), 7)]

    for week in weeks:
        week_cols = st.columns(7)
        for col, day in zip(week_cols, week):
            with col:
                if day == "":
                    st.markdown('<div style="height:44px;"></div>', unsafe_allow_html=True)
                    continue

                d = date(year, month, day)
                day_str = str(d)
                status = cal_data.get(day_str, "none")
                is_today = d == today

                color_map = {
                    "complete": ("#10b981", "rgba(16,185,129,0.2)", "rgba(16,185,129,0.4)"),
                    "partial": ("#f59e0b", "rgba(245,158,11,0.15)", "rgba(245,158,11,0.3)"),
                    "missed": ("#f43f5e", "rgba(244,63,94,0.1)", "rgba(244,63,94,0.2)"),
                    "future": ("#475569", "rgba(255,255,255,0.03)", "rgba(255,255,255,0.06)"),
                    "none": ("#64748b", "rgba(255,255,255,0.03)", "rgba(255,255,255,0.06)"),
                }
                text_color, bg_color, border_color = color_map.get(status, color_map["none"])
                today_border = f"2px solid #8b5cf6" if is_today else f"1px solid {border_color}"
                font_weight = "800" if is_today else "600"

                emoji_map = {"complete": "✓", "partial": "◐", "missed": "✗", "future": "", "none": ""}
                status_char = emoji_map.get(status, "")

                st.markdown(f"""
                <div style="width:100%;aspect-ratio:1;background:{bg_color};border:{today_border};
                    border-radius:10px;display:flex;flex-direction:column;align-items:center;
                    justify-content:center;cursor:pointer;transition:transform 0.15s;
                    min-height:44px;position:relative;">
                    <span style="font-size:0.88rem;font-weight:{font_weight};color:{text_color};">{day}</span>
                    {f'<span style="font-size:0.6rem;color:{text_color};position:absolute;bottom:4px;">{status_char}</span>' if status_char else ''}
                </div>""", unsafe_allow_html=True)

    # Monthly stats
    st.markdown("<br>", unsafe_allow_html=True)
    stat_cols = st.columns(4)
    complete_days = sum(1 for v in cal_data.values() if v == "complete")
    partial_days = sum(1 for v in cal_data.values() if v == "partial")
    missed_days = sum(1 for v in cal_data.values() if v == "missed")
    none_days = sum(1 for v in cal_data.values() if v == "none")

    month_stats = [
        ("✅ Complete", complete_days, "#10b981"),
        ("◐ Partial", partial_days, "#f59e0b"),
        ("✗ Missed", missed_days, "#f43f5e"),
        ("— No data", none_days, "#475569"),
    ]
    for col, (label, count, color) in zip(stat_cols, month_stats):
        with col:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                border-radius:12px;padding:1rem;text-align:center;">
                <div style="font-size:1.5rem;font-weight:800;color:{color};">{count}</div>
                <div style="font-size:0.75rem;color:#64748b;margin-top:0.25rem;">{label}</div>
            </div>""", unsafe_allow_html=True)

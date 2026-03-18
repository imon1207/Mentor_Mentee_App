"""Sessions — view, filter, and manage mentoring sessions."""
import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.data_loader import load_sessions, load_mentors, load_mentees


def status_badge(s: str) -> str:
    color = {"Completed": "#3fb950", "Scheduled": "#58a6ff",
             "Cancelled": "#f78166", "No-show": "#d29922"}.get(s, "#8b949e")
    return f'<span style="color:{color}; font-weight:600">{s}</span>'


def render():
    st.title("📅 Sessions")
    st.markdown("Browse, filter, and inspect mentoring sessions.")

    sessions = load_sessions()
    mentors  = load_mentors()
    mentees  = load_mentees()

    # ── Filters ────────────────────────────────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        status_filter = st.multiselect("Status", sessions["status"].unique().tolist(),
                                       default=sessions["status"].unique().tolist())
    with col2:
        domain_opts = ["All"] + sorted(sessions["domain"].unique().tolist())
        domain_filter = st.selectbox("Domain", domain_opts)
    with col3:
        min_date = sessions["session_date"].min().date()
        max_date = sessions["session_date"].max().date()
        date_range = st.date_input("Date range", [min_date, max_date])
    with col4:
        dur_filter = st.multiselect("Duration (min)", sorted(sessions["duration_min"].unique()), default=[])

    df = sessions.copy()
    if status_filter:
        df = df[df["status"].isin(status_filter)]
    if domain_filter != "All":
        df = df[df["domain"] == domain_filter]
    if len(date_range) == 2:
        df = df[(df["session_date"].dt.date >= date_range[0]) &
                (df["session_date"].dt.date <= date_range[1])]
    if dur_filter:
        df = df[df["duration_min"].isin(dur_filter)]

    # ── KPIs ───────────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Filtered Sessions", len(df))
    c2.metric("Avg Duration (min)", f"{df['duration_min'].mean():.0f}" if len(df) else "—")
    c3.metric("Avg Rating", f"{df['rating_given'].dropna().mean():.2f}" if len(df) else "—")
    c4.metric("Completion Rate", f"{(df['status']=='Completed').mean()*100:.1f}%" if len(df) else "—")

    st.divider()

    # ── Table ──────────────────────────────────────────────────────────────────
    show_cols = ["session_id", "mentor_name", "mentee_name", "domain",
                 "session_date", "duration_min", "status", "rating_given", "notes"]
    display = df[show_cols].copy()
    display["session_date"] = display["session_date"].dt.strftime("%Y-%m-%d")
    display = display.reset_index(drop=True)
    display.index += 1

    st.dataframe(display, use_container_width=True, height=400)

    st.divider()

    # ── Session detail ─────────────────────────────────────────────────────────
    st.subheader("🔎 Session Detail")
    sid_list = df["session_id"].tolist()
    if sid_list:
        chosen = st.selectbox("Select a session to inspect", sid_list)
        row = df[df["session_id"] == chosen].iloc[0]

        cc1, cc2 = st.columns(2)
        with cc1:
            st.markdown(f"**Session ID:** `{row['session_id']}`")
            st.markdown(f"**Mentor:** {row['mentor_name']} (`{row['mentor_id']}`)")
            st.markdown(f"**Mentee:** {row['mentee_name']} (`{row['mentee_id']}`)")
            st.markdown(f"**Domain:** {row['domain']}")
        with cc2:
            st.markdown(f"**Date:** {row['session_date'].strftime('%B %d, %Y')}")
            st.markdown(f"**Duration:** {row['duration_min']} minutes")
            st.markdown(f"**Status:** {row['status']}")
            st.markdown(f"**Rating:** {'⭐ ' + str(row['rating_given']) if pd.notna(row['rating_given']) else 'Not rated'}")
        if row["notes"]:
            st.info(f"📝 **Notes:** {row['notes']}")

    # ── Upcoming sessions ──────────────────────────────────────────────────────
    st.divider()
    st.subheader("🗓️ Upcoming Scheduled Sessions")
    upcoming = (sessions[sessions["status"] == "Scheduled"]
                .sort_values("session_date")
                .head(10)[["session_id","mentor_name","mentee_name","domain","session_date","duration_min"]])
    upcoming["session_date"] = upcoming["session_date"].dt.strftime("%Y-%m-%d")
    st.dataframe(upcoming.reset_index(drop=True), use_container_width=True)

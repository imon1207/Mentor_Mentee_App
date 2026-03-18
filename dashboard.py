"""Dashboard — platform overview & quick stats."""
import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.data_loader import load_mentors, load_mentees, load_sessions, load_messages


def render():
    st.title("🏠 Dashboard")
    st.markdown("Welcome back! Here's your platform at a glance.")

    mentors  = load_mentors()
    mentees  = load_mentees()
    sessions = load_sessions()
    messages = load_messages()

    completed = sessions[sessions["status"] == "Completed"]
    avg_rating = completed["rating_given"].dropna().mean()

    # ── KPI row ───────────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("👨‍🏫 Mentors",          f"{len(mentors):,}")
    c2.metric("🎓 Mentees",           f"{len(mentees):,}")
    c3.metric("📅 Total Sessions",    f"{len(sessions):,}")
    c4.metric("✅ Completed",         f"{len(completed):,}")
    c5.metric("⭐ Avg Rating",        f"{avg_rating:.2f}")

    st.divider()

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader("📈 Monthly Session Trend")
        monthly = (sessions.copy()
                   .assign(month=sessions["session_date"].dt.to_period("M").astype(str))
                   .groupby("month").size().reset_index(name="Sessions"))
        st.line_chart(monthly.set_index("month")["Sessions"])

    with col_right:
        st.subheader("🗂️ Sessions by Domain")
        domain_cnt = (sessions.groupby("domain").size()
                      .reset_index(name="count")
                      .sort_values("count", ascending=False)
                      .head(8))
        st.bar_chart(domain_cnt.set_index("domain")["count"])

    st.divider()

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("🌟 Top Rated Mentors")
        top = (mentors.sort_values(["rating", "total_sessions"], ascending=False)
               .head(5)[["name", "domain", "rating", "total_sessions", "experience_years"]]
               .reset_index(drop=True))
        top.index += 1
        st.dataframe(top, use_container_width=True)

    with col_b:
        st.subheader("💬 Recent Messages")
        recent_msgs = (messages.sort_values("timestamp", ascending=False)
                       .head(6)[["sender_name", "sender_type", "message", "timestamp"]]
                       .reset_index(drop=True))
        recent_msgs["timestamp"] = recent_msgs["timestamp"].dt.strftime("%b %d, %H:%M")
        st.dataframe(recent_msgs, use_container_width=True)

    st.divider()
    st.subheader("📊 Session Status Breakdown")
    status_counts = sessions["status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    st.bar_chart(status_counts.set_index("Status")["Count"])

"""Profile — view any mentor or mentee profile."""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.data_loader import load_mentors, load_mentees, load_sessions, load_messages


def render():
    st.title("👤 Profile Viewer")

    role = st.radio("View profile of:", ["Mentor", "Mentee"], horizontal=True)
    mentors  = load_mentors()
    mentees  = load_mentees()
    sessions = load_sessions()
    messages = load_messages()

    if role == "Mentor":
        people = mentors.copy()
        id_col = "mentor_id"
        choices = {row[id_col]: f"{row['name']} ({row['domain']})" for _, row in people.iterrows()}
        selected_id = st.selectbox("Select a Mentor", list(choices.keys()), format_func=lambda x: choices[x])

        if selected_id:
            p = people[people[id_col] == selected_id].iloc[0]
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"## {p['name']}")
                st.markdown(f"**Domain:** {p['domain']}  |  **Country:** {p['country']}  |  **Gender:** {p['gender']}")
                st.markdown(f"**Bio:** {p['bio']}")
                st.markdown(f"**Skills:** `{p['skills']}`")
                st.markdown(f"**LinkedIn:** [{p['linkedin']}](https://{p['linkedin']})")
                st.markdown(f"**Joined:** {p['joined_date']}")
            with c2:
                st.metric("⭐ Rating", p["rating"])
                st.metric("🧑‍💼 Experience", f"{p['experience_years']} yrs")
                st.metric("📅 Total Sessions", p["total_sessions"])
                st.metric("💰 Rate", "Free" if p["session_rate_usd"] == 0 else f"${int(p['session_rate_usd'])}/hr")
                st.metric("🕐 Availability", p["availability"])
                st.metric("👥 Max Mentees", p["max_mentees"])

            st.divider()
            st.subheader("Recent Sessions")
            m_sessions = sessions[sessions["mentor_id"] == selected_id].sort_values("session_date", ascending=False).head(10)
            if not m_sessions.empty:
                disp = m_sessions[["session_id","mentee_name","domain","session_date","status","rating_given","duration_min"]].copy()
                disp["session_date"] = disp["session_date"].dt.strftime("%Y-%m-%d")
                st.dataframe(disp.reset_index(drop=True), use_container_width=True)
            else:
                st.info("No sessions found.")

            st.subheader("Recent Messages Sent")
            m_msgs = messages[messages["mentor_id"] == selected_id].sort_values("timestamp", ascending=False).head(10)
            if not m_msgs.empty:
                disp = m_msgs[["message","timestamp","session_id","sender_type"]].copy()
                disp["timestamp"] = disp["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
                st.dataframe(disp.reset_index(drop=True), use_container_width=True)
            else:
                st.info("No messages found.")

    else:  # Mentee
        people = mentees.copy()
        id_col = "mentee_id"
        choices = {row[id_col]: f"{row['name']} ({row['domain_interest']})" for _, row in people.iterrows()}
        selected_id = st.selectbox("Select a Mentee", list(choices.keys()), format_func=lambda x: choices[x])

        if selected_id:
            p = people[people[id_col] == selected_id].iloc[0]
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"## {p['name']}")
                st.markdown(f"**Domain Interest:** {p['domain_interest']}  |  **Country:** {p['country']}  |  **Gender:** {p['gender']}")
                st.markdown(f"**Goal:** {p['goal']}")
                st.markdown(f"**Current Skills:** `{p['current_skills']}`")
                st.markdown(f"**Joined:** {p['joined_date']}")
            with c2:
                st.metric("📊 Experience", p["experience_level"])
                st.metric("🕐 Availability", p["availability"])
                st.metric("💰 Budget", f"${p['budget_usd']}/session" if p["budget_usd"] > 0 else "Free only")
                st.metric("👤 Gender Pref", p["preferred_gender"])

            st.divider()
            st.subheader("Session History")
            t_sessions = sessions[sessions["mentee_id"] == selected_id].sort_values("session_date", ascending=False).head(10)
            if not t_sessions.empty:
                disp = t_sessions[["session_id","mentor_name","domain","session_date","status","rating_given","duration_min"]].copy()
                disp["session_date"] = disp["session_date"].dt.strftime("%Y-%m-%d")
                st.dataframe(disp.reset_index(drop=True), use_container_width=True)
            else:
                st.info("No sessions found.")

            st.subheader("Messages Sent")
            t_msgs = messages[messages["mentee_id"] == selected_id].sort_values("timestamp", ascending=False).head(10)
            if not t_msgs.empty:
                disp = t_msgs[["message","timestamp","session_id","sender_type"]].copy()
                disp["timestamp"] = disp["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
                st.dataframe(disp.reset_index(drop=True), use_container_width=True)
            else:
                st.info("No messages found.")

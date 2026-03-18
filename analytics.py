"""Analytics — charts & insights from the dataset."""
import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.data_loader import load_mentors, load_mentees, load_sessions, load_messages


def render():
    st.title("📊 Analytics")
    st.markdown("Deep-dive insights across the platform.")

    mentors  = load_mentors()
    mentees  = load_mentees()
    sessions = load_sessions()
    messages = load_messages()

    tabs = st.tabs(["🧑‍🏫 Mentors", "🎓 Mentees", "📅 Sessions", "💬 Messages"])

    # ── Mentors ────────────────────────────────────────────────────────────────
    with tabs[0]:
        st.subheader("Mentor Distribution by Domain")
        dom = mentors["domain"].value_counts().reset_index()
        dom.columns = ["Domain", "Count"]
        st.bar_chart(dom.set_index("Domain")["Count"])

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Experience Level")
            exp = mentors["expertise_level"].value_counts().reset_index()
            exp.columns = ["Level", "Count"]
            st.bar_chart(exp.set_index("Level")["Count"])
        with col2:
            st.subheader("Session Rate Distribution (USD)")
            rate = mentors["session_rate_usd"].value_counts().sort_index().reset_index()
            rate.columns = ["Rate", "Count"]
            st.bar_chart(rate.set_index("Rate")["Count"])

        st.subheader("Top Countries")
        countries = mentors["country"].value_counts().head(10).reset_index()
        countries.columns = ["Country", "Mentors"]
        st.bar_chart(countries.set_index("Country")["Mentors"])

        st.subheader("Rating Distribution")
        rating_bins = mentors["rating"].round(0).value_counts().sort_index().reset_index()
        rating_bins.columns = ["Rating", "Count"]
        st.bar_chart(rating_bins.set_index("Rating")["Count"])

    # ── Mentees ────────────────────────────────────────────────────────────────
    with tabs[1]:
        st.subheader("Mentee Domain Interest")
        di = mentees["domain_interest"].value_counts().reset_index()
        di.columns = ["Domain", "Count"]
        st.bar_chart(di.set_index("Domain")["Count"])

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Experience Level")
            el = mentees["experience_level"].value_counts().reset_index()
            el.columns = ["Level", "Count"]
            st.bar_chart(el.set_index("Level")["Count"])
        with col2:
            st.subheader("Budget Range (USD)")
            bd = mentees["budget_usd"].value_counts().sort_index().reset_index()
            bd.columns = ["Budget", "Count"]
            st.bar_chart(bd.set_index("Budget")["Count"])

        st.subheader("Mentee Availability")
        av = mentees["availability"].value_counts().reset_index()
        av.columns = ["Availability", "Count"]
        st.bar_chart(av.set_index("Availability")["Count"])

    # ── Sessions ───────────────────────────────────────────────────────────────
    with tabs[2]:
        st.subheader("Sessions Over Time (Monthly)")
        monthly = (sessions.assign(month=sessions["session_date"].dt.to_period("M").astype(str))
                   .groupby("month").size().reset_index(name="Sessions"))
        st.line_chart(monthly.set_index("month")["Sessions"])

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Status Breakdown")
            sb = sessions["status"].value_counts().reset_index()
            sb.columns = ["Status", "Count"]
            st.bar_chart(sb.set_index("Status")["Count"])
        with col2:
            st.subheader("Duration Distribution (min)")
            dur = sessions["duration_min"].value_counts().sort_index().reset_index()
            dur.columns = ["Duration", "Count"]
            st.bar_chart(dur.set_index("Duration")["Count"])

        st.subheader("Average Rating per Domain")
        domain_rating = (sessions.dropna(subset=["rating_given"])
                         .groupby("domain")["rating_given"].mean()
                         .reset_index())
        domain_rating.columns = ["Domain", "Avg Rating"]
        st.bar_chart(domain_rating.set_index("Domain")["Avg Rating"])

        st.subheader("Completion Rate per Domain")
        sessions["completed"] = sessions["status"] == "Completed"
        comp_rate = sessions.groupby("domain")["completed"].mean().reset_index()
        comp_rate.columns = ["Domain", "Completion Rate"]
        comp_rate["Completion Rate"] = (comp_rate["Completion Rate"] * 100).round(1)
        st.bar_chart(comp_rate.set_index("Domain")["Completion Rate"])

    # ── Messages ───────────────────────────────────────────────────────────────
    with tabs[3]:
        st.subheader("Messages Per Day")
        messages["date"] = messages["timestamp"].dt.date
        daily = messages.groupby("date").size().reset_index(name="Messages")
        daily["date"] = daily["date"].astype(str)
        st.line_chart(daily.set_index("date")["Messages"])

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Sender Type Split")
            st.metric("Mentor messages", len(messages[messages["sender_type"] == "mentor"]))
            st.metric("Mentee messages", len(messages[messages["sender_type"] == "mentee"]))
        with col2:
            st.subheader("Read vs Unread")
            read_counts = messages["read"].value_counts().reset_index()
            read_counts.columns = ["Read", "Count"]
            read_counts["Read"] = read_counts["Read"].map({True: "Read", False: "Unread"})
            st.bar_chart(read_counts.set_index("Read")["Count"])

        st.subheader("Top Active Sessions (by message count)")
        top_sess = messages.groupby("session_id").size().reset_index(name="Messages")
        top_sess = top_sess.sort_values("Messages", ascending=False).head(10)
        st.bar_chart(top_sess.set_index("session_id")["Messages"])

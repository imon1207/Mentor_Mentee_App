"""Find a Mentor — browse & smart-match mentors."""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.data_loader import load_mentors, load_mentees, match_mentors

DOMAINS = ["All", "Data Science", "Web Development", "Machine Learning",
           "Cybersecurity", "Cloud Computing", "DevOps", "UI/UX Design",
           "Mobile Development", "Blockchain", "Product Management"]


def star_row(rating: float) -> str:
    full = int(rating)
    half = 1 if (rating - full) >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + "½" * half + "☆" * empty


def render():
    st.title("🔍 Find a Mentor")

    tab1, tab2 = st.tabs(["🧭 Smart Match", "📋 Browse All"])

    # ── Smart Match ────────────────────────────────────────────────────────────
    with tab1:
        st.markdown("### Tell us about yourself")
        mentees = load_mentees()
        mentors = load_mentors()

        c1, c2 = st.columns(2)
        with c1:
            domain = st.selectbox("Your domain of interest", DOMAINS[1:])
            availability = st.selectbox("Your availability", ["Weekdays","Weekends","Evenings","Flexible","Mornings"])
            budget = st.slider("Max budget (USD/session)", 0, 150, 0, step=10)
        with c2:
            exp_level = st.selectbox("Your experience level", ["Beginner","Intermediate","Advanced"])
            gender_pref = st.selectbox("Preferred mentor gender", ["No preference","Male","Female"])
            goal = st.text_area("Your goal (optional)", placeholder="e.g. Land a data science job in 6 months")

        if st.button("🚀 Find My Matches", use_container_width=True):
            pseudo_mentee = {
                "domain_interest":  domain,
                "availability":     availability,
                "budget_usd":       budget,
                "experience_level": exp_level,
                "preferred_gender": gender_pref,
            }
            import pandas as pd
            matches = match_mentors(pd.Series(pseudo_mentee), mentors, top_n=5)
            st.success(f"Found **{len(matches)}** best matches for you!")

            for _, m in matches.iterrows():
                score_pct = int(min(m["match_score"] / 12 * 100, 100))
                with st.container():
                    st.markdown(f"""
<div class="mentor-card">
  <div style="display:flex; justify-content:space-between; align-items:start">
    <div>
      <h4 style="margin:0; color:#58a6ff">{m['name']}</h4>
      <span style="color:#8b949e; font-size:13px">{m['domain']} · {m['country']}</span>
    </div>
    <span class="score-badge">Match {score_pct}%</span>
  </div>
  <p style="margin:8px 0 4px 0; font-size:13px">{m['bio']}</p>
  <div style="display:flex; gap:16px; font-size:13px; color:#8b949e; flex-wrap:wrap; margin-top:6px">
    <span>⭐ {m['rating']}</span>
    <span>🧑‍💼 {m['experience_years']} yrs</span>
    <span>🕐 {m['availability']}</span>
    <span>💰 {'Free' if m['session_rate_usd']==0 else f"${int(m['session_rate_usd'])}/session"}</span>
    <span>📅 {m['total_sessions']} sessions done</span>
  </div>
  <div style="margin-top:8px; font-size:12px; color:#8b949e">🔧 {m['skills']}</div>
</div>
""", unsafe_allow_html=True)

    # ── Browse All ─────────────────────────────────────────────────────────────
    with tab2:
        mentors = load_mentors()
        col1, col2, col3 = st.columns(3)
        with col1:
            domain_filter = st.selectbox("Domain", DOMAINS, key="browse_domain")
        with col2:
            avail_filter = st.selectbox("Availability", ["All","Weekdays","Weekends","Evenings","Flexible","Mornings"])
        with col3:
            sort_by = st.selectbox("Sort by", ["Rating", "Experience", "Sessions Done"])

        df = mentors.copy()
        if domain_filter != "All":
            df = df[df["domain"] == domain_filter]
        if avail_filter != "All":
            df = df[df["availability"] == avail_filter]

        sort_col = {"Rating": "rating", "Experience": "experience_years", "Sessions Done": "total_sessions"}[sort_by]
        df = df.sort_values(sort_col, ascending=False).reset_index(drop=True)

        st.markdown(f"**{len(df)} mentors found**")
        st.divider()

        for _, m in df.head(20).iterrows():
            with st.expander(f"👤 {m['name']}  —  {m['domain']}  |  ⭐ {m['rating']}  |  {m['experience_years']} yrs exp"):
                cc1, cc2 = st.columns([2, 1])
                with cc1:
                    st.markdown(f"**Bio:** {m['bio']}")
                    st.markdown(f"**Skills:** `{m['skills']}`")
                    st.markdown(f"**LinkedIn:** {m['linkedin']}")
                with cc2:
                    st.metric("Rating", m["rating"])
                    st.metric("Sessions", m["total_sessions"])
                    st.metric("Rate", "Free" if m["session_rate_usd"] == 0 else f"${int(m['session_rate_usd'])}/hr")
                st.caption(f"Country: {m['country']} · Availability: {m['availability']} · Max mentees: {m['max_mentees']}")

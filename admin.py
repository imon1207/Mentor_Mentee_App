"""Admin Panel — full platform control for administrators."""
import streamlit as st
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.data_loader import load_mentors, load_mentees, load_sessions, load_messages

USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "users.csv")


def render():
    st.title("🛡️ Admin Panel")
    st.markdown(f"Welcome, **{st.session_state.get('name','Admin')}** · Full platform access")

    mentors  = load_mentors()
    mentees  = load_mentees()
    sessions = load_sessions()
    messages = load_messages()

    # ── Platform KPIs ─────────────────────────────────────────────────────────
    st.subheader("📊 Platform Overview")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("👨‍🏫 Mentors",        len(mentors))
    c2.metric("🎓 Mentees",          len(mentees))
    c3.metric("📅 Sessions",         len(sessions))
    c4.metric("✅ Completed",        len(sessions[sessions["status"]=="Completed"]))
    c5.metric("💬 Messages",         len(messages))
    c6.metric("⭐ Avg Rating",       f"{sessions['rating_given'].dropna().mean():.2f}")

    st.divider()

    tabs = st.tabs(["👨‍🏫 Mentors", "🎓 Mentees", "📅 Sessions", "💬 Messages", "👥 Users", "📈 Reports"])

    # ── Mentors Tab ────────────────────────────────────────────────────────────
    with tabs[0]:
        st.subheader("All Mentor Records")
        col1, col2 = st.columns(2)
        with col1:
            domain_f = st.selectbox("Filter by Domain", ["All"] + sorted(mentors["domain"].unique()), key="adm_dom")
        with col2:
            search_m = st.text_input("Search by Name", placeholder="Type a name...", key="adm_msrch")

        df = mentors.copy()
        if domain_f != "All":
            df = df[df["domain"] == domain_f]
        if search_m:
            df = df[df["name"].str.contains(search_m, case=False)]

        st.markdown(f"**{len(df)} mentors**")
        st.dataframe(df.reset_index(drop=True), use_container_width=True, height=350)

        st.subheader("📊 Mentor Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**By Domain**")
            st.bar_chart(mentors["domain"].value_counts())
        with col2:
            st.markdown("**By Country**")
            st.bar_chart(mentors["country"].value_counts().head(8))

        st.markdown("**Rating Distribution**")
        st.bar_chart(mentors["rating"].round(0).value_counts().sort_index())

        st.subheader("🏆 Top 10 Mentors by Rating")
        top = mentors.sort_values(["rating","total_sessions"], ascending=False).head(10)[
            ["mentor_id","name","domain","rating","experience_years","total_sessions","country","session_rate_usd"]
        ].reset_index(drop=True)
        top.index += 1
        st.dataframe(top, use_container_width=True)

    # ── Mentees Tab ────────────────────────────────────────────────────────────
    with tabs[1]:
        st.subheader("All Mentee Records")
        col1, col2 = st.columns(2)
        with col1:
            domain_t = st.selectbox("Filter by Domain", ["All"] + sorted(mentees["domain_interest"].unique()), key="adm_tdom")
        with col2:
            search_t = st.text_input("Search by Name", placeholder="Type a name...", key="adm_tsrch")

        dft = mentees.copy()
        if domain_t != "All":
            dft = dft[dft["domain_interest"] == domain_t]
        if search_t:
            dft = dft[dft["name"].str.contains(search_t, case=False)]

        st.markdown(f"**{len(dft)} mentees**")
        st.dataframe(dft.reset_index(drop=True), use_container_width=True, height=350)

        st.subheader("📊 Mentee Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**By Domain Interest**")
            st.bar_chart(mentees["domain_interest"].value_counts())
        with col2:
            st.markdown("**By Experience Level**")
            st.bar_chart(mentees["experience_level"].value_counts())

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**By Country**")
            st.bar_chart(mentees["country"].value_counts().head(8))
        with col2:
            st.markdown("**Budget Distribution**")
            st.bar_chart(mentees["budget_usd"].value_counts().sort_index())

    # ── Sessions Tab ───────────────────────────────────────────────────────────
    with tabs[2]:
        st.subheader("All Sessions")
        col1, col2 = st.columns(2)
        with col1:
            status_f = st.multiselect("Status", sessions["status"].unique().tolist(),
                                      default=sessions["status"].unique().tolist(), key="adm_stat")
        with col2:
            domain_sf = st.selectbox("Domain", ["All"] + sorted(sessions["domain"].unique()), key="adm_sdom")

        dfs = sessions.copy()
        if status_f:
            dfs = dfs[dfs["status"].isin(status_f)]
        if domain_sf != "All":
            dfs = dfs[dfs["domain"] == domain_sf]

        disp = dfs[["session_id","mentor_name","mentee_name","domain","session_date","duration_min","status","rating_given"]].copy()
        disp["session_date"] = disp["session_date"].dt.strftime("%Y-%m-%d")
        st.markdown(f"**{len(disp)} sessions**")
        st.dataframe(disp.reset_index(drop=True), use_container_width=True, height=350)

        st.subheader("📊 Session Trends")
        monthly = (sessions.assign(month=sessions["session_date"].dt.to_period("M").astype(str))
                   .groupby("month").size().reset_index(name="Sessions"))
        st.line_chart(monthly.set_index("month")["Sessions"])

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Status Breakdown**")
            st.bar_chart(sessions["status"].value_counts())
        with col2:
            st.markdown("**Avg Rating per Domain**")
            dr = sessions.dropna(subset=["rating_given"]).groupby("domain")["rating_given"].mean()
            st.bar_chart(dr)

    # ── Messages Tab ───────────────────────────────────────────────────────────
    with tabs[3]:
        st.subheader("All Messages")
        search_msg = st.text_input("Search message content", placeholder="Search...", key="adm_msgsrch")
        dfm = messages.copy()
        if search_msg:
            dfm = dfm[dfm["message"].str.contains(search_msg, case=False)]

        disp_m = dfm[["message_id","sender_name","sender_type","message","timestamp","session_id","read"]].copy()
        disp_m["timestamp"] = disp_m["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
        st.markdown(f"**{len(disp_m)} messages**")
        st.dataframe(disp_m.reset_index(drop=True), use_container_width=True, height=350)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Messages per Day**")
            messages["date"] = messages["timestamp"].dt.date.astype(str)
            st.line_chart(messages.groupby("date").size())
        with col2:
            st.markdown("**Read vs Unread**")
            rv = messages["read"].map({True:"Read", False:"Unread"}).value_counts()
            st.bar_chart(rv)

    # ── Users Tab ──────────────────────────────────────────────────────────────
    with tabs[4]:
        st.subheader("👥 Registered Users")
        users_df = pd.read_csv(USERS_FILE)
        # Never show passwords in plain text
        safe = users_df[["username","role","name","email"]].copy()
        st.dataframe(safe, use_container_width=True)

        st.divider()
        st.subheader("➕ Add New User")
        col1, col2 = st.columns(2)
        with col1:
            new_user  = st.text_input("Username")
            new_pass  = st.text_input("Password", type="password")
            new_role  = st.selectbox("Role", ["mentor","mentee","admin"])
        with col2:
            new_name  = st.text_input("Full Name")
            new_email = st.text_input("Email")

        if st.button("Add User", use_container_width=True):
            if new_user and new_pass and new_name and new_email:
                if new_user in users_df["username"].values:
                    st.error("Username already exists!")
                else:
                    new_row = pd.DataFrame([{
                        "username": new_user, "password": new_pass,
                        "role": new_role, "name": new_name, "email": new_email
                    }])
                    updated = pd.concat([users_df, new_row], ignore_index=True)
                    updated.to_csv(USERS_FILE, index=False)
                    st.success(f"✅ User '{new_user}' added as {new_role}!")
                    st.rerun()
            else:
                st.warning("Please fill all fields.")

        st.divider()
        st.subheader("🗑️ Remove User")
        non_admin = users_df[users_df["role"] != "admin"]["username"].tolist()
        del_user = st.selectbox("Select user to remove", non_admin)
        if st.button("Remove User", use_container_width=True):
            updated = users_df[users_df["username"] != del_user]
            updated.to_csv(USERS_FILE, index=False)
            st.success(f"User '{del_user}' removed.")
            st.rerun()

    # ── Reports Tab ────────────────────────────────────────────────────────────
    with tabs[5]:
        st.subheader("📈 Platform Health Report")

        total_s   = len(sessions)
        completed = len(sessions[sessions["status"]=="Completed"])
        cancelled = len(sessions[sessions["status"]=="Cancelled"])
        comp_rate = completed / total_s * 100 if total_s else 0
        canc_rate = cancelled / total_s * 100 if total_s else 0
        avg_dur   = sessions["duration_min"].mean()
        avg_rat   = sessions["rating_given"].dropna().mean()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Completion Rate", f"{comp_rate:.1f}%")
        col2.metric("Cancellation Rate", f"{canc_rate:.1f}%")
        col3.metric("Avg Session Duration", f"{avg_dur:.0f} min")
        col4.metric("Platform Avg Rating", f"{avg_rat:.2f} ⭐")

        st.divider()
        st.subheader("Domain Performance")
        domain_perf = (sessions.groupby("domain").agg(
            Total=("session_id","count"),
            Completed=("status", lambda x: (x=="Completed").sum()),
            Avg_Rating=("rating_given","mean"),
        ).round(2).reset_index())
        domain_perf["Completion%"] = (domain_perf["Completed"] / domain_perf["Total"] * 100).round(1)
        st.dataframe(domain_perf, use_container_width=True)

        st.subheader("Mentor Engagement")
        mentor_eng = (sessions.groupby(["mentor_id","mentor_name"]).agg(
            Sessions=("session_id","count"),
            Completed=("status", lambda x: (x=="Completed").sum()),
            Avg_Rating=("rating_given","mean"),
        ).round(2).reset_index().sort_values("Sessions", ascending=False).head(15))
        st.dataframe(mentor_eng, use_container_width=True)

        st.subheader("Monthly Growth")
        monthly = (sessions.assign(month=sessions["session_date"].dt.to_period("M").astype(str))
                   .groupby("month").size().reset_index(name="Sessions"))
        st.line_chart(monthly.set_index("month"))

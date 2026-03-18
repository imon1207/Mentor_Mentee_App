"""Login page — handles authentication for all roles."""
import streamlit as st
import pandas as pd
import os

USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "users.csv")


def load_users() -> pd.DataFrame:
    return pd.read_csv(USERS_FILE)


def render():
    # ── Centered login card ────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding: 40px 0 10px 0;">
        <div style="font-size:64px">🎓</div>
        <h1 style="font-family:'Syne',sans-serif; font-size:2.8rem; margin:0; color:#58a6ff;">MentorNet</h1>
        <p style="color:#8b949e; font-size:1.1rem; margin-top:6px;">Connecting minds, shaping futures</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style="background:#161b22; border:1px solid #30363d; border-radius:16px; padding:32px 28px; margin-top:10px;">
        """, unsafe_allow_html=True)

        st.markdown("### 🔐 Sign In")
        st.caption("Use your credentials to access the platform")

        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", placeholder="Enter your password", type="password")

        role_hint = st.empty()

        if st.button("Login →", use_container_width=True):
            if not username or not password:
                st.error("Please enter both username and password.")
            else:
                users = load_users()
                match = users[(users["username"] == username) & (users["password"] == password)]
                if not match.empty:
                    user = match.iloc[0]
                    st.session_state["logged_in"] = True
                    st.session_state["username"]  = user["username"]
                    st.session_state["role"]       = user["role"]
                    st.session_state["name"]       = user["name"]
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.divider()
        st.markdown("**Demo credentials:**")
        demo_data = {
            "Role":     ["Admin",     "Mentor",   "Mentee"],
            "Username": ["admin",     "mentor1",  "mentee1"],
            "Password": ["admin123",  "mentor123","mentee123"],
        }
        st.table(pd.DataFrame(demo_data))

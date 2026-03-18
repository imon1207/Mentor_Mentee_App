"""
MentorNet — Mentor-Mentee Communication Platform
Main entry point: streamlit run app.py
"""
import streamlit as st

st.set_page_config(
    page_title="MentorNet",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=Inter:wght@300;400;500;600&display=swap');
:root {
  --bg:#0d1117; --card:#161b22; --border:#30363d; --accent:#58a6ff;
  --accent2:#f78166; --accent3:#3fb950; --text:#e6edf3; --muted:#8b949e; --radius:12px;
}
html, body, [class*="css"] { background-color:var(--bg)!important; color:var(--text)!important; font-family:'Inter',sans-serif; }
h1,h2,h3 { font-family:'Syne',sans-serif; }
section[data-testid="stSidebar"] { background:var(--card)!important; border-right:1px solid var(--border); }
[data-testid="stMetric"] { background:var(--card); border:1px solid var(--border); border-radius:var(--radius); padding:14px 18px; }
[data-testid="stMetricValue"] { color:var(--accent)!important; font-family:'Syne',sans-serif; }
.stButton > button { background:var(--accent)!important; color:#0d1117!important; border:none!important; border-radius:8px!important; font-weight:600!important; padding:8px 20px!important; transition:opacity .2s; }
.stButton > button:hover { opacity:.85!important; }
.bubble-mentor { background:#1e3a5f; border-left:3px solid var(--accent); padding:10px 14px; border-radius:0 12px 12px 12px; margin:6px 0; max-width:78%; }
.bubble-mentee { background:#1e3325; border-right:3px solid var(--accent3); padding:10px 14px; border-radius:12px 0 12px 12px; margin:6px 0 6px auto; max-width:78%; text-align:right; }
.bubble-time { font-size:11px; color:var(--muted); margin-top:3px; }
.mentor-card { background:var(--card); border:1px solid var(--border); border-radius:var(--radius); padding:18px; margin-bottom:14px; transition:border-color .2s; }
.mentor-card:hover { border-color:var(--accent); }
.score-badge { background:var(--accent); color:#0d1117; border-radius:20px; padding:2px 10px; font-size:12px; font-weight:700; }
[data-baseweb="tab-list"] { background:transparent!important; }
[data-baseweb="tab"] { color:var(--muted)!important; }
[aria-selected="true"] { color:var(--accent)!important; border-bottom-color:var(--accent)!important; }
input,textarea,select { background:var(--card)!important; color:var(--text)!important; border-color:var(--border)!important; border-radius:8px!important; }
[data-testid="stDataFrame"] { border-radius:var(--radius); overflow:hidden; }
.role-badge-admin  { background:#f78166; color:#0d1117; padding:2px 10px; border-radius:20px; font-size:12px; font-weight:700; }
.role-badge-mentor { background:#58a6ff; color:#0d1117; padding:2px 10px; border-radius:20px; font-size:12px; font-weight:700; }
.role-badge-mentee { background:#3fb950; color:#0d1117; padding:2px 10px; border-radius:20px; font-size:12px; font-weight:700; }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    from _pages import login
    login.render()
    st.stop()

role = st.session_state["role"]
name = st.session_state.get("name", "User")

with st.sidebar:
    st.markdown("## 🎓 MentorNet")
    st.markdown("*Connecting minds, shaping futures*")
    st.divider()
    badge_class = f"role-badge-{role}"
    st.markdown(f"👤 **{name}**  <span class='{badge_class}'>{role.upper()}</span>", unsafe_allow_html=True)
    st.divider()

    if role == "admin":
        pages = ["🏠 Dashboard","🛡️ Admin Panel","🔍 Find a Mentor","💬 Messages","📅 Sessions","📊 Analytics","👤 Profile"]
    elif role == "mentor":
        pages = ["🏠 Dashboard","💬 Messages","📅 Sessions","📊 Analytics","👤 Profile"]
    else:
        pages = ["🏠 Dashboard","🔍 Find a Mentor","💬 Messages","📅 Sessions","👤 Profile"]

    page = st.radio("Navigate", pages)
    st.divider()
    if st.button("🚪 Logout", use_container_width=True):
        for key in ["logged_in","role","name","username"]:
            st.session_state.pop(key, None)
        st.rerun()
    st.caption("Dataset: Kaggle-style Mentorship Data\n700 mentors/mentees · 1K sessions · 2K messages")

page_key = page.split(" ", 1)[1]

if page_key == "Dashboard":
    from _pages import dashboard; dashboard.render()
elif page_key == "Admin Panel":
    from _pages import admin; admin.render()
elif page_key == "Find a Mentor":
    from _pages import find_mentor; find_mentor.render()
elif page_key == "Messages":
    from _pages import messages; messages.render()
elif page_key == "Sessions":
    from _pages import sessions; sessions.render()
elif page_key == "Analytics":
    from _pages import analytics; analytics.render()
elif page_key == "Profile":
    from _pages import profile; profile.render()

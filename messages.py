"""Messages — real-time style chat between mentor & mentee."""
import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.data_loader import load_sessions, load_messages, append_message


def render():
    st.title("💬 Messages")
    st.markdown("Send and receive messages with your mentor / mentee.")

    sessions = load_sessions()
    messages = load_messages()

    # ── Role selector ──────────────────────────────────────────────────────────
    col_a, col_b = st.columns([2, 1])
    with col_a:
        role = st.radio("You are a:", ["Mentor", "Mentee"], horizontal=True)
    with col_b:
        st.caption("Pick a session thread below to chat.")

    # ── Session chooser ────────────────────────────────────────────────────────
    completed = sessions[sessions["status"].isin(["Completed", "Scheduled"])]
    sample = completed.head(30)

    session_labels = {
        row["session_id"]: f"{row['session_id']} · {row['mentor_name']} ↔ {row['mentee_name']} ({row['domain']}) — {row['session_date'].strftime('%b %d %Y')}"
        for _, row in sample.iterrows()
    }
    selected_sid = st.selectbox("Choose a session thread", list(session_labels.keys()),
                                format_func=lambda x: session_labels[x])

    if not selected_sid:
        st.info("No session selected.")
        return

    sess_row = sample[sample["session_id"] == selected_sid].iloc[0]
    mentor_id   = sess_row["mentor_id"]
    mentee_id   = sess_row["mentee_id"]
    mentor_name = sess_row["mentor_name"]
    mentee_name = sess_row["mentee_name"]

    sender_type = role.lower()
    sender_name = mentor_name if sender_type == "mentor" else mentee_name

    st.divider()
    st.markdown(f"**Thread:** {mentor_name} (Mentor) ↔ {mentee_name} (Mentee)  |  Domain: `{sess_row['domain']}`")

    # ── Chat thread ────────────────────────────────────────────────────────────
    thread = messages[messages["session_id"] == selected_sid].sort_values("timestamp")

    chat_html = ""
    for _, msg in thread.iterrows():
        ts = msg["timestamp"].strftime("%b %d, %H:%M")
        if msg["sender_type"] == "mentor":
            chat_html += f"""
<div class="bubble-mentor">
  <strong style="color:#58a6ff; font-size:13px">👨‍🏫 {msg['sender_name']}</strong><br>
  {msg['message']}
  <div class="bubble-time">{ts}</div>
</div>"""
        else:
            chat_html += f"""
<div class="bubble-mentee">
  <strong style="color:#3fb950; font-size:13px">{msg['sender_name']} 🎓</strong><br>
  {msg['message']}
  <div class="bubble-time">{ts}</div>
</div>"""

    if not thread.empty:
        st.markdown(f'<div style="max-height:420px; overflow-y:auto; padding:8px;">{chat_html}</div>',
                    unsafe_allow_html=True)
    else:
        st.info("No messages yet in this thread. Start the conversation below!")

    st.divider()

    # ── Compose ────────────────────────────────────────────────────────────────
    with st.form("compose_form", clear_on_submit=True):
        new_msg = st.text_area(f"✍️ Your message as **{sender_name}** ({role})", height=80,
                               placeholder="Type your message…")
        sent = st.form_submit_button("Send 📤", use_container_width=True)
        if sent:
            if new_msg.strip():
                append_message(
                    session_id=selected_sid,
                    mentor_id=mentor_id,
                    mentee_id=mentee_id,
                    sender_type=sender_type,
                    sender_name=sender_name,
                    message=new_msg.strip(),
                    mentor_name=mentor_name,
                    mentee_name=mentee_name,
                )
                st.success("Message sent! Refresh to see it in the thread.")
            else:
                st.warning("Cannot send an empty message.")

    # ── Quick stats ────────────────────────────────────────────────────────────
    st.divider()
    st.subheader("📊 Message Statistics")
    cc1, cc2, cc3 = st.columns(3)
    cc1.metric("Total in Thread", len(thread))
    cc2.metric("From Mentor", len(thread[thread["sender_type"] == "mentor"]))
    cc3.metric("From Mentee",  len(thread[thread["sender_type"] == "mentee"]))

    st.subheader("All Platform Messages (Recent 50)")
    recent = (messages.sort_values("timestamp", ascending=False)
              .head(50)[["sender_name", "sender_type", "message", "timestamp", "session_id"]]
              .reset_index(drop=True))
    recent["timestamp"] = recent["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
    st.dataframe(recent, use_container_width=True, height=300)

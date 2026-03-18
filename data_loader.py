"""
Data loading & helper utilities — no SQL, pure pandas/CSV.
"""
import os
import pandas as pd
import json
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
MSG_FILE = os.path.join(DATA_DIR, "messages.csv")


# ── CSV loaders ───────────────────────────────────────────────────────────────
def load_mentors() -> pd.DataFrame:
    return pd.read_csv(os.path.join(DATA_DIR, "mentors.csv"))


def load_mentees() -> pd.DataFrame:
    return pd.read_csv(os.path.join(DATA_DIR, "mentees.csv"))


def load_sessions() -> pd.DataFrame:
    df = pd.read_csv(os.path.join(DATA_DIR, "sessions.csv"))
    df["session_date"] = pd.to_datetime(df["session_date"])
    return df


def load_messages() -> pd.DataFrame:
    df = pd.read_csv(MSG_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


# ── Matching helper ───────────────────────────────────────────────────────────
def match_mentors(mentee_row: pd.Series, mentors: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    """Rule-based mentor matching without ML."""
    df = mentors.copy()
    score = pd.Series(0, index=df.index)

    # Domain match (most important)
    score += (df["domain"] == mentee_row["domain_interest"]).astype(int) * 5

    # Availability match
    score += (df["availability"] == mentee_row["availability"]).astype(int) * 3

    # Budget match (free sessions preferred if budget is 0)
    if mentee_row["budget_usd"] == 0:
        score += (df["session_rate_usd"] == 0).astype(int) * 2
    else:
        score += (df["session_rate_usd"] <= mentee_row["budget_usd"]).astype(int) * 2

    # Gender preference
    if mentee_row.get("preferred_gender", "No preference") != "No preference":
        score += (df["gender"] == mentee_row["preferred_gender"]).astype(int) * 1

    # Add rating boost
    score += (df["rating"] / 5).round(2)

    df["match_score"] = score
    return df.sort_values("match_score", ascending=False).head(top_n)


# ── Message persistence ───────────────────────────────────────────────────────
def append_message(session_id: str, mentor_id: str, mentee_id: str,
                   sender_type: str, sender_name: str, message: str,
                   mentor_name: str = "", mentee_name: str = ""):
    """Append a new message row to messages.csv."""
    df = load_messages()
    new_id = f"MSG{len(df)+1:05d}"
    new_row = {
        "message_id":  new_id,
        "session_id":  session_id,
        "mentor_id":   mentor_id,
        "mentee_id":   mentee_id,
        "sender_type": sender_type,
        "sender_name": sender_name,
        "message":     message,
        "timestamp":   datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "read":        False,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(MSG_FILE, index=False)
    return new_id


def get_thread(session_id: str) -> pd.DataFrame:
    """Return all messages for a session, sorted by time."""
    df = load_messages()
    return df[df["session_id"] == session_id].sort_values("timestamp")


# ── Analytics helpers ─────────────────────────────────────────────────────────
def sessions_by_domain(sessions: pd.DataFrame) -> pd.DataFrame:
    return sessions.groupby("domain").size().reset_index(name="count")


def rating_distribution(sessions: pd.DataFrame) -> pd.DataFrame:
    return sessions["rating_given"].dropna()


def monthly_sessions(sessions: pd.DataFrame) -> pd.DataFrame:
    s = sessions.copy()
    s["month"] = s["session_date"].dt.to_period("M").astype(str)
    return s.groupby("month").size().reset_index(name="sessions")


def top_mentors(mentors: pd.DataFrame, sessions: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    cnt = sessions[sessions["status"] == "Completed"].groupby("mentor_id").size().reset_index(name="completed")
    merged = mentors.merge(cnt, on="mentor_id", how="left").fillna(0)
    merged["completed"] = merged["completed"].astype(int)
    return merged.sort_values(["rating", "completed"], ascending=False).head(n)

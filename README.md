# 🎓 MentorNet — Mentor-Mentee Communication Platform

A Streamlit web application for mentorship management, smart matching, and real-time-style messaging. Built with Python, pandas, and Streamlit — **no SQL, no database** required.

---

## 📁 Project Structure

```
mentor_mentee/
├── app.py                    # Main entry point
├── requirements.txt
├── data/
│   ├── generate_data.py      # Kaggle-style synthetic dataset generator
│   ├── mentors.csv           # 200 mentor profiles
│   ├── mentees.csv           # 500 mentee profiles
│   ├── sessions.csv          # 1,000 mentoring sessions
│   └── messages.csv          # 2,000 chat messages
├── pages/
│   ├── dashboard.py          # Platform KPIs & trends
│   ├── find_mentor.py        # Smart match + browse
│   ├── messages.py           # Chat interface
│   ├── sessions.py           # Session management
│   ├── analytics.py          # Charts & insights
│   └── profile.py            # User profile viewer
├── utils/
│   └── data_loader.py        # CSV I/O & business logic
└── .vscode/
    └── launch.json           # VS Code run config
```

---

## 🚀 Quick Start

### 1 — Clone / open folder in VS Code
```bash
cd mentor_mentee
```

### 2 — Create a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### 4 — Generate the dataset (first time only)
```bash
python data/generate_data.py
```

### 5 — Run the app
```bash
streamlit run app.py
```
Open **http://localhost:8501** in your browser.

> In VS Code you can also press **F5** with the `.vscode/launch.json` config selected.

---

## 📊 Dataset (Kaggle-mirrored)

| File | Rows | Key columns |
|------|------|-------------|
| `mentors.csv` | 200 | mentor_id, name, domain, skills, rating, experience_years, session_rate_usd |
| `mentees.csv` | 500 | mentee_id, name, domain_interest, experience_level, budget_usd |
| `sessions.csv` | 1,000 | session_id, mentor_id, mentee_id, session_date, status, rating_given |
| `messages.csv` | 2,000 | message_id, session_id, sender_type, message, timestamp, read |

All data stored as **CSV** — zero SQL, zero ORM.

---

## ✨ Features

| Page | What it does |
|------|-------------|
| 🏠 Dashboard | KPI cards, monthly trend, top mentors, recent messages |
| 🔍 Find a Mentor | Rule-based smart matching (domain, availability, budget, gender) + full browse |
| 💬 Messages | Per-session chat thread with send capability (persisted to CSV) |
| 📅 Sessions | Filter by status/domain/date, session detail view |
| 📊 Analytics | 15+ charts across mentors, mentees, sessions, messages |
| 👤 Profile | Full profile for any mentor or mentee with history |

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** — UI framework
- **Pandas** — all data manipulation (no SQL)
- **NumPy** — synthetic data generation

---

## 📌 Notes

- Messages are **persisted** by appending rows to `messages.csv`.
- Matching algorithm is rule-based (weighted scoring on domain, availability, budget, gender preference, and rating).
- To regenerate fresh data: `python data/generate_data.py` (overwrites CSVs).

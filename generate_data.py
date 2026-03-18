"""
Dataset generator for Mentor-Mentee Communication Platform
Mirrors structure from Kaggle mentorship/education datasets
"""
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

# ── Domains & Skills ──────────────────────────────────────────────────────────
DOMAINS = ["Data Science", "Web Development", "Machine Learning",
           "Cybersecurity", "Cloud Computing", "DevOps", "UI/UX Design",
           "Mobile Development", "Blockchain", "Product Management"]

SKILLS_MAP = {
    "Data Science":        ["Python", "R", "SQL", "Tableau", "Statistics", "Pandas", "Scikit-learn"],
    "Web Development":     ["HTML", "CSS", "JavaScript", "React", "Node.js", "Django", "Vue.js"],
    "Machine Learning":    ["TensorFlow", "PyTorch", "Keras", "OpenCV", "NLP", "Deep Learning"],
    "Cybersecurity":       ["Penetration Testing", "SIEM", "Forensics", "Network Security", "Ethical Hacking"],
    "Cloud Computing":     ["AWS", "Azure", "GCP", "Kubernetes", "Docker", "Terraform"],
    "DevOps":              ["CI/CD", "Jenkins", "Git", "Ansible", "Monitoring", "Shell Scripting"],
    "UI/UX Design":        ["Figma", "Adobe XD", "Wireframing", "User Research", "Prototyping"],
    "Mobile Development":  ["Flutter", "React Native", "Swift", "Kotlin", "Android", "iOS"],
    "Blockchain":          ["Solidity", "Ethereum", "Smart Contracts", "Web3.js", "DeFi"],
    "Product Management":  ["Agile", "Scrum", "Roadmapping", "User Stories", "OKRs", "Jira"],
}

AVAILABILITY = ["Weekdays", "Weekends", "Evenings", "Flexible", "Mornings"]
EXPERIENCE_LEVELS = ["Beginner", "Intermediate", "Advanced", "Expert"]
GENDERS = ["Male", "Female", "Non-binary", "Prefer not to say"]
COUNTRIES = ["India", "USA", "UK", "Canada", "Australia", "Germany",
             "Nigeria", "Brazil", "Singapore", "France"]

FIRST_NAMES = ["Arjun","Priya","Liam","Emma","Noah","Olivia","Aarav","Zara",
               "Carlos","Sofia","James","Aisha","Wei","Fatima","Lucas","Amara",
               "Daniel","Nadia","Kiran","Sarah","Michael","Riya","Ahmed","Elena",
               "Rohan","Mei","Tyler","Kofi","Isabelle","Raj","Hannah","Omar",
               "Divya","Ethan","Sana","Yusuf","Chloe","Ivan","Pooja","Alex"]
LAST_NAMES  = ["Sharma","Patel","Smith","Johnson","Lee","Kim","Wang","Garcia",
               "Müller","Osei","Silva","Tremblay","Kumar","Ali","Rossi","Brown",
               "Davis","Wilson","Taylor","Anderson","Martinez","Thompson","White",
               "Harris","Clark","Lewis","Robinson","Walker","Hall","Young"]

def rnd_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def rnd_skills(domain, n=3):
    pool = SKILLS_MAP.get(domain, [])
    return ", ".join(random.sample(pool, min(n, len(pool))))

# ── Mentors (200 rows) ────────────────────────────────────────────────────────
def build_mentors(n=200):
    rows = []
    for i in range(1, n+1):
        domain = random.choice(DOMAINS)
        exp_yrs = random.randint(3, 20)
        rows.append({
            "mentor_id":          f"M{i:04d}",
            "name":               rnd_name(),
            "email":              f"mentor{i}@mentornet.io",
            "gender":             random.choice(GENDERS),
            "country":            random.choice(COUNTRIES),
            "domain":             domain,
            "skills":             rnd_skills(domain, random.randint(3,5)),
            "experience_years":   exp_yrs,
            "expertise_level":    "Expert" if exp_yrs > 12 else ("Advanced" if exp_yrs > 7 else "Intermediate"),
            "availability":       random.choice(AVAILABILITY),
            "max_mentees":        random.randint(2, 6),
            "session_rate_usd":   random.choice([0, 0, 20, 30, 50, 75, 100]),
            "rating":             round(random.uniform(3.5, 5.0), 1),
            "total_sessions":     random.randint(10, 300),
            "bio":                f"Passionate {domain} professional with {exp_yrs}+ years of industry experience.",
            "linkedin":           f"linkedin.com/in/mentor{i}",
            "joined_date":        (datetime(2020,1,1) + timedelta(days=random.randint(0,1200))).strftime("%Y-%m-%d"),
        })
    return pd.DataFrame(rows)

# ── Mentees (500 rows) ────────────────────────────────────────────────────────
def build_mentees(n=500):
    rows = []
    for i in range(1, n+1):
        domain = random.choice(DOMAINS)
        rows.append({
            "mentee_id":          f"T{i:04d}",
            "name":               rnd_name(),
            "email":              f"mentee{i}@mentornet.io",
            "gender":             random.choice(GENDERS),
            "country":            random.choice(COUNTRIES),
            "domain_interest":    domain,
            "current_skills":     rnd_skills(domain, random.randint(1,3)),
            "goal":               f"Improve {domain} skills and land a job in {random.choice(['6','12','18'])} months.",
            "experience_level":   random.choice(EXPERIENCE_LEVELS[:3]),
            "availability":       random.choice(AVAILABILITY),
            "budget_usd":         random.choice([0, 20, 50, 100, 150]),
            "preferred_gender":   random.choice(["No preference", "Male", "Female"]),
            "joined_date":        (datetime(2021,1,1) + timedelta(days=random.randint(0,900))).strftime("%Y-%m-%d"),
        })
    return pd.DataFrame(rows)

# ── Sessions (1 000 rows) ─────────────────────────────────────────────────────
def build_sessions(mentors, mentees, n=1000):
    rows = []
    statuses = ["Completed","Completed","Completed","Scheduled","Cancelled","No-show"]
    for i in range(1, n+1):
        mentor = mentors.sample(1).iloc[0]
        mentee = mentees.sample(1).iloc[0]
        date   = datetime(2022,1,1) + timedelta(days=random.randint(0,730))
        rows.append({
            "session_id":      f"S{i:05d}",
            "mentor_id":       mentor["mentor_id"],
            "mentee_id":       mentee["mentee_id"],
            "mentor_name":     mentor["name"],
            "mentee_name":     mentee["name"],
            "domain":          mentor["domain"],
            "session_date":    date.strftime("%Y-%m-%d"),
            "duration_min":    random.choice([30, 45, 60, 90]),
            "status":          random.choice(statuses),
            "rating_given":    round(random.uniform(3,5),1) if random.random() > 0.3 else None,
            "notes":           random.choice(["Discussed portfolio review","Covered system design","Code review session",
                                              "Career roadmap planning","Mock interview","Project feedback",""]),
        })
    return pd.DataFrame(rows)

# ── Messages (2 000 rows) ─────────────────────────────────────────────────────
MESSAGES = [
    "Hi! Looking forward to our session.", "Can we reschedule to next week?",
    "Thank you for the great session!", "I have a question about the assignment.",
    "Please review my GitHub repo.", "I completed the task you suggested!",
    "Could you share some resources on this topic?", "Our call is confirmed for tomorrow.",
    "I need help with my resume.", "The feedback was very helpful, thank you!",
    "Can we focus on interview prep next time?", "I finished the online course you recommended.",
    "Looking forward to connecting soon.", "I have updated my LinkedIn as advised.",
    "Can you check my project structure?",
]

def build_messages(mentors, mentees, sessions, n=2000):
    rows = []
    for i in range(1, n+1):
        s = sessions.sample(1).iloc[0]
        sender_type = random.choice(["mentor","mentee"])
        msg_date = (datetime.strptime(s["session_date"],"%Y-%m-%d")
                    + timedelta(days=random.randint(-3,3)))
        rows.append({
            "message_id":   f"MSG{i:05d}",
            "session_id":   s["session_id"],
            "mentor_id":    s["mentor_id"],
            "mentee_id":    s["mentee_id"],
            "sender_type":  sender_type,
            "sender_name":  s["mentor_name"] if sender_type=="mentor" else s["mentee_name"],
            "message":      random.choice(MESSAGES),
            "timestamp":    msg_date.strftime("%Y-%m-%d %H:%M:%S"),
            "read":         random.choice([True, True, False]),
        })
    return pd.DataFrame(rows)

# ── Build & Save ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    out = os.path.dirname(__file__)
    print("Generating data...")
    mentors  = build_mentors()
    mentees  = build_mentees()
    sessions = build_sessions(mentors, mentees)
    messages = build_messages(mentors, mentees, sessions)

    mentors .to_csv(f"{out}/mentors.csv",  index=False)
    mentees .to_csv(f"{out}/mentees.csv",  index=False)
    sessions.to_csv(f"{out}/sessions.csv", index=False)
    messages.to_csv(f"{out}/messages.csv", index=False)
    print(f"✅ mentors.csv    → {len(mentors)} rows")
    print(f"✅ mentees.csv    → {len(mentees)} rows")
    print(f"✅ sessions.csv   → {len(sessions)} rows")
    print(f"✅ messages.csv   → {len(messages)} rows")

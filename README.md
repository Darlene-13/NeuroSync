# 🧠 Neuro_Sync: Your AI-Powered Discipline Engine

![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Active%20Development-blue)
![MadeWith](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)

> 🚀 *Dream big. Plan smart. Stay consistent.*  
> Neuro_Sync is your intelligent, gamified productivity assistant that helps you manage time, track progress, and build discipline through the power of AI.

---

## 📌 Table of Contents

- [✨ Key Features](#-key-features)
- [📸 Screenshots](#-screenshots)
- [⚙️ How It Works](#️-how-it-works)
- [🧠 AI Capabilities](#-ai-capabilities)
- [🏁 Getting Started](#-getting-started)
- [🛠️ Tech Stack](#️-tech-stack)
- [📚 File Structure](#-file-structure)
- [📈 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [🛡 License](#-license)

---

## ✨ Key Features

### 🔹 Planning & Productivity
- AI-powered smart scheduler (GPT + Claude)
- Mood-based planning (light vs heavy tasks)
- School/freelance project planner
- Pomodoro/focus timer
- Calendar sync & Gmail integration

### 🔹 Gamification & Motivation
- XP system, achievement badges, personal challenges
- Leaderboards, streaks, reward system

### 🔹 AI Brain
- Custom GPT & Claude API integration
- Learning path optimization (e.g., coding)
- Memory-aware context planning

### 🔹 Finance & Life Tracking
- Expense and budget tracking
- Financial goal management
- Trend analysis and reports

### 🔹 Multi-Platform Support
- Web dashboard (Flask)
- Desktop GUI (Tkinter)
- CLI interface
- Telegram, WhatsApp bot
- Voice support (coming soon)

### 🔹 Automation & Notifications
- Gmail, Telegram, desktop alerts
- Sync with Google Drive & Calendar
- Daily/weekly backup + AI summaries

---

## 📸 Screenshots

> *(Coming soon — See `/docs/images/screenshots/` for previews)*

---

## ⚙️ How It Works

Neuro_Sync merges **behavioral science** and **machine learning** to help you build routines, beat procrastination, and execute on long-term goals — consistently.

1. Add your tasks, habits, goals, and schedules.
2. The AI suggests how to prioritize them intelligently.
3. Earn XP, unlock achievements, and stay motivated.
4. Get daily summaries, performance analytics, and real-time alerts.

---

## 🧠 AI Capabilities

| Feature | Description |
|--------|-------------|
| `Smart Planner` | Suggests optimal task order based on time, mood, urgency |
| `Learning Optimizer` | Recommends coding topics, study plans |
| `Custom GPT` | Context-aware assistant trained on your data |
| `Mood Analyzer` | Adjusts suggestions based on journal or emoji log |
| `Claude & GPT failover` | Switches intelligently when one model fails |

---

## 🏁 Getting Started

### 1. Clone the repository


### 2. Create a virtual environment
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
### 3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
#### 4. Set up environment variables
bash
Copy
Edit
cp .env.template .env
# Fill in your OpenAI, Claude, Gmail, etc.
### 5. Launch the app
bash
Copy
Edit
python main.py
🧪 Run python scripts/setup_environment.py for interactive config.

### 🛠️ Tech Stack
Layer - Technologies
Backend	- Python, Flask, SQLite, SQLAlchemy
AI Brain - OpenAI API, Claude API, custom GPT logic
GUI	Tkinter - (desktop), HTML/CSS/JS (web)
Notifications - Gmail SMTP, Telegram Bot API, Twilio WhatsApp
DevOps	Docker, GitHub Actions, .env, backup scripts

### 📚 File Structure
Full breakdown available in docs/architecture/system_design.md

bash
Copy
Edit
Neuro_Sync/
├── core/            # Task, habit, finance logic
├── ai/              # AI planner, mood analyzer, custom GPT
├── gamification/    # XP, badges, challenges
├── interfaces/      # CLI, GUI, Web, Bots
├── notifications/   # Alerts via email, bots, desktop
├── analytics/       # Trend detection, reporting
├── sync/            # Gmail, Google Calendar, Drive sync
├── templates/       # Flask HTML templates
├── static/          # CSS, JS, sounds
├── data/            # SQLite DB, JSON, backups
├── tests/           # Unit + integration tests
├── scripts/         # Setup, backup, export utilities
└── docs/            # Architecture, API, dev guides


 📈 Roadmap
 #### AI-powered planning

 #### XP + achievement system

 #### CLI, desktop, web support

 #### Gmail/Telegram/WhatsApp alerts

####  Mood-aware suggestions

 Mobile PWA wrapper

 Team mode: shared boards

 Voice interface (OpenVoice SDK)

 API gateway + OAuth login

### 🤝 Contributing
#### We love contributors! To get started:

#### Fork the repo

#### Create a feature branch

#### Push your changes

#### Submit a pull request

#### Please read CONTRIBUTING.md for our code of conduct and best practices.

### 🛡 License
This project is licensed under the MIT License.
See LICENSE for full text.

💬 Built with 💙 by Darlene & contributors
✨ Empowering dreamers to become doers — one task at a time.

yaml
Copy
Edit

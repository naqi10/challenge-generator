# 💻 AI-Powered Coding Challenge Generator

An interactive web app to generate multiple-choice coding challenges based on difficulty levels using OpenAI's API. Built with **React.js (Frontend)** and **FastAPI (Backend)**.

---

---

## 🧠 Features

- 🎯 Generate coding questions dynamically based on difficulty.
- 🤖 Uses OpenAI API (GPT-3.5 Turbo) for realistic coding MCQs.
- 📊 Tracks user quota and auto-resets daily.
- 🧩 Clean and simple interface for practicing questions.
- ✅ Auth-ready using Clerk (optional).

---

## 🛠️ Tech Stack

| Frontend  | Backend | AI Engine | Auth (optional) |
|-----------|---------|-----------|-----------------|
| React.js  | FastAPI | OpenAI API | Clerk           |

---

## 📁 Folder Structure

challenge-generator/
│
├── backend/
│   ├── src/
│   │   ├── routes/
│   │   │   └── __init__.py
│   │   │   └── your_api_routes.py
│   │   │
│   │   ├── database/
│   │   │   └── models.py
│   │   │   └── db_init.py
│   │   │
│   │   ├── core/                # New: config, security, helpers
│   │   │   └── config.py
│   │   │   └── utils.py
│   │   │
│   │   ├── services/            # New: business logic
│   │   │   └── ai_generator.py
│   │   │   └── challenge_service.py
│   │   │
│   │   ├── main.py              # renamed from app.py (standard for FastAPI)
│   │   └── __init__.py
│   │   └── .env
│   │
│   ├── database.db
│   ├── pyproject.toml
│   ├── uv.lock
│   ├── .gitignore
│   ├── .python-version
│   └── server.py                # Optional: Uvicorn entry point
│
├── frontend/
│   ├── public/
│   ├── node_modules/
│   ├── src/
│   │   ├── auth/
│   │   │   └── AuthenticationPage.jsx
│   │   │   └── ClerkProviderWithRoutes.jsx
│   │   │
│   │   ├── challenge/
│   │   │   └── ChallengeGenerator.jsx
│   │   │   └── MCQChallenge.jsx
│   │   │
│   │   ├── layout/
│   │   │   └── Layout.jsx
│   │   │
│   │   ├── history/
│   │   ├── assets/              # New: images, logos, icons
│   │   ├── components/          # New: reusable UI components
│   │   └── App.jsx
│   │   └── index.jsx
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── .gitignore
│
├── README.md
└── .gitignore



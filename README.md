# NoteVault API

A secure backend API for managing personal notes with user accounts, built using FastAPI, SQLAlchemy, PostgreSQL, and Alembic.

This project is being developed in **phases** to ensure clean architecture, proper separation of concerns, and production-ready practices.

---

## 🚀 Tech Stack

- **FastAPI**
- **SQLAlchemy (ORM)**
- **PostgreSQL**
- **Alembic (Database Migrations)**
- **Passlib (Argon2 password hashing)**

---


## 🧱 Implemented Phases

### ✅ Phase 1 — Notes CRUD
- Create, read, update, delete notes
- PostgreSQL-backed persistence
- Proper schemas and error handling
- No authentication

### ✅ Phase 2 — Users
- User model with email and role
- Secure password hashing (Argon2)
- User CRUD endpoints
- Alembic migrations applied
- No authentication yet (by design)

---

## 🔐 Security Notes

- Passwords are **hashed**, never stored or exposed in plaintext
- Sensitive configuration is handled via `.env` (not committed)
- Alembic configuration is committed without secrets

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone <your-repo-url>
cd notevault-api

2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Configure environment variables

Create a .env file:

DATABASE_URL=postgresql://username:password@localhost:5432/notevault

5️⃣ Run database migrations
alembic upgrade head

6️⃣ Start the server
uvicorn app.main:app --reload

🧪 Database State

After migrations, the following tables exist:

notevault

users

alembic_version
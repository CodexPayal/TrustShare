# 🔐 TrustShare — Authentication Module

**TrustShare** is a secure file-sharing system developed as part of the **Infosys Springboard Virtual Internship 7.0**.

This repository contains the backend implementation of the **Authentication Module**, providing secure user authentication, authorization, password recovery, and session management.

## ✨ Authentication Features

* 👤 User Registration
* 🔑 User Login
* 🚪 User Logout
* ♻️ Refresh Token
* 🔐 JWT Authentication
* 🛡️ Role-Based Access Control (RBAC)
* 🔒 Multi-Factor Authentication (MFA)
* 🌐 Google OAuth / OAuth2
* 📧 Forgot Password
* 🔄 Reset Password
* ⚡ Session Management
* 🚀 Redis Session Support

## 🗄️ Database

* **Users Table** — Stores user account and authentication information.
* **Sessions Table** — Manages authenticated user sessions.

## 🛡️ Security

* 🔒 **bcrypt** — Secure password hashing
* 🔑 **JWT** — Token-based authentication
* 🌐 **OAuth2** — Secure external authentication
* ⚡ **Redis** — Session management
* 🔐 **Secure Reset Tokens** — Password recovery workflow
* 🛡️ **RBAC** — Role-based authorization
* 🔐 **MFA** — Additional authentication layer

## 🛠️ Tech Stack

| Technology               | Purpose             |
| ------------------------ | ------------------- |
| 🐍 Python                | Backend Development |
| ⚡ FastAPI                | REST API Framework  |
| 🗄️ PostgreSQL           | Database            |
| 🔗 SQLAlchemy            | ORM                 |
| 🔑 JWT                   | Authentication      |
| 🔒 bcrypt                | Password Hashing    |
| 🌐 OAuth2 / Google OAuth | Authentication      |
| ⚡ Redis                  | Session Management  |
| 🚀 Uvicorn               | Application Server  |

## 📂 Project Structure

```text id="3t8x8w"
backend/
└── app/
    ├── main.py
    │
    ├── models/
    │   ├── __init__.py
    │   ├── user.py
    │   └── session.py
    │
    ├── routes/
    │   └── auth.py
    │
    ├── schemas/
    │   └── user.py
    │
    ├── security/
    │   ├── jwt.py
    │   └── reset_token.py
    │
    └── services/
        ├── mfa.py
        ├── redis_client.py
        └── session.py
```

## 🚀 Setup

### Clone Repository

```bash id="j9q7gk"
git clone https://github.com/CodexPayal/TrustShare.git
cd TrustShare/backend
```

### Create Virtual Environment

```bash id="z2r2f9"
python -m venv venv
```

### Activate Virtual Environment

**Windows:**

```powershell id="8ymg7y"
.\venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash id="7y8fba"
pip install -r requirements.txt
```

### Environment Configuration

Configure the required PostgreSQL, JWT, Google OAuth, and Redis credentials in the `.env` file.

> ⚠️ Never commit secrets, passwords, API keys, or `.env` files to the repository.

### Run the Backend

```bash id="j2a1d5"
uvicorn app.main:app --reload
```

## 📚 API Documentation

FastAPI provides interactive API documentation through Swagger UI:

```text id="6d6s2c"
http://127.0.0.1:8000/docs
```

ReDoc:

```text id="v1u2hm"
http://127.0.0.1:8000/redoc
```

## 🔄 Authentication Flow

```text id="6l1h0k"
Register
   ↓
Login
   ↓
JWT + Session
   ↓
Protected Resources
   ↓
Refresh Token
   ↓
New Access Token
   ↓
Logout
```

Password recovery:

```text id="wzv4p9"
Forgot Password
      ↓
Reset Token
      ↓
Token Validation
      ↓
New Password
```

## 🎓 Internship Context

**Program:** Infosys Springboard Virtual Internship 7.0
**Project:** TrustShare — Secure File-Sharing System
**Module:** Authentication Module
**Backend:** Python + FastAPI

## 👩‍💻 Author

**Priyank Swain**

**Reshma Challa**

**Infosys Springboard Virtual Internship 7.0 — Project Contributor**
